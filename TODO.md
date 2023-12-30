## TODOs

- [ ] Keep track of prices and show average price of all printed proxies
- [ ] Implement "Export as.." on /ui/api/proxies
- [ ] Implement remote logging
- [ ] Support PTCGL basic energy format (4 Basic {P} Energy SVE 5, 2 Basic {P} Energy CRZ 156)
- [ ] Properly support both PTCGL and PTCGO decklist formats
- [ ] Edit decklist hack using "history.back()" doesn't work reliably
- [ ] Support Shiny Vault cards (They seem to not have a standard set id?, some say they're part of the main set they
  belong to, some say they belong to their own set: sm1)
- [ ] BREAK and LEGEND cards don't work properly in text mode with illustrations enabled
- [ ] Text mode only supports 1 deck at a time (should support 3)
- [ ] Redesign features page?
- [ ] Make a database table for card issues so that the table can be automatically generated
- [ ] Make some kind of utility to add records to the above table (manage.py like program)
- [ ] Add the sentry feedback form thing to error pages
- [ ] AUTOMATED TESTING
- [ ] Maybe don't create the share by default. Only create the share when the "share deck" button is clicked
- [ ] The build hash doesn't work in github actions
- [ ] Tools that have attacks (TMs, forest seal, etc.) look weird in text mode
- [ ] Cards with multiple subtypes (e.g. forest seal stone being both item and tool) only show a single type
- [ ] Create alt set codes for some sets (like PR-SW should also have SSP (at least according to limitlesstcg))
- [ ] Combine the "build" and "notify" jobs into one workflow so that the notification only happens if the build succeeds 

## IP

- [~] Implement "generate from URL options"

## FIRST PASS DONE

- [X] Implement single click bookmarklet
- [X] Implement sentry support
- [X] Implement logging
- [X] Refactor all the text on the website that changed (such as links, email addrs, and changed features like "up to
  3 decklists")

## DONE

- [X] Implement some kind of bg job that runs on a timer to update the database
- [X] Make a background job that deletes expired shares
- [X] Convert the full list of set codes from a google sheet to a webpage with a table
- [X] Convert the missing cards from a google sheet to a webpage with a table
- [X] Make some kind of way to enable "maintenance mode" so that the main webserver only hosts the "under maintenance"
  page automatically
- [X] Set discord link on the changelog page
- [X] Write dotenv.template
- [X] Write dockerfile to build a docker container to serve the app
- [X] Bots are spamming the database with random shit. There needs to be some kind of validation for creating a shared
  deck
- [X] Leading spaces in the decklist breaks the entire thing
- [X] TODO: Include the build number in the version file? (the container hash maybe?). This is to be specific with which
  build is currently active. This is to prevent stupid issues with caching on cloudflare.
- [X] Using leading zeros in the card count breaks things
- [X] Items, special energies, supporters, and stadiums don't work in text mode


## NOT DOING

- [X] Add todo/known issues page? (Already exists in help page)

## MISSING CARDS:

- hsp-HGSS18
- xyp-XY39 doesn't have a high-res image
- xyp-XY46 doesn't have a high-res image
- xyp-XY68 doesn't have a high-res image
- ALL OF mcd14
- ALL OF mcd15
- ALL OF mcd17
- ALL OF mcd18

