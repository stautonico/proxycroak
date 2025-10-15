{
  description = "Proxycroak dev shell (Python 3.13, Zsh, Docker MySQL)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python313;
      in {
        devShells.default = pkgs.mkShell {
          name = "proxycroak-dev";

          buildInputs = [
            python
            pkgs.python313Packages.virtualenv
            pkgs.python313Packages.pip
            pkgs.zsh
            pkgs.docker
            pkgs.docker-compose
            pkgs.mysql-client
          ];

          shellHook = ''
            export SHELL=$(which zsh)

            # Create and activate Python venv
            if [ ! -d .venv ]; then
              python -m venv .venv
            fi
            source .venv/bin/activate

            # Sync dependencies
            pip install --upgrade pip wheel setuptools pip-tools >/dev/null
            pip install -r requirements.txt

            # Start MySQL container
            docker-compose up -d proxycroak-db-development || true

            # Project-specific ZDOTDIR
            PROJECT_ZDOTDIR="$(pwd)/.nix-zdotdir"
            mkdir -p "$PROJECT_ZDOTDIR"

            # Single-quoted heredoc so Nix doesn't expand $ or *
            cat > "$PROJECT_ZDOTDIR/.zshrc" <<'EOF'
            # Load Oh My Zsh (with Agnoster)
            if [ -f "$HOME/.oh-my-zsh/oh-my-zsh.sh" ]; then
              source "$HOME/.oh-my-zsh/oh-my-zsh.sh"
            fi

            # Only for interactive shells
            if [[ $- == *i* ]]; then
              # Green venv indicator on the right
              if [ -d ".venv" ]; then
                RPROMPT="%F{green}(proxycroak venv)%f"
              fi
              trap 'echo "🧹 Stopping MySQL container..."; docker-compose down' EXIT

              # ✅ Add MySQL alias using env vars
              if [[ -n "$DB_HOST" && -n "$DB_USER" && -n "$DB_PASS" ]]; then
                alias db='mysql --protocol=TCP -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS"'
              else
                alias db='echo "❌ Missing DB_* variables in .env"'
              fi

              alias runpc='flask --app "proxycroak:create_app" run --debug'
              echo -e "\033[1;31m🔥 Type \"runpc\" to start the app!\033[0m"
              echo -e "\033[1;34m🐬 Type \"db\" to connect to your Docker MySQL database.\033[0m"
            fi
            EOF

            export ZDOTDIR="$PROJECT_ZDOTDIR"

            if [ -f .env ]; then
              export $(grep -v '^#' .env | xargs)
            fi



            echo "⚙️ Launching Zsh with Agnoster RPROMPT override..."
            exec zsh -i
          '';
        };
      });
}
