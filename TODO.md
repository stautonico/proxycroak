## TODOs

- [ ] Keep track of prices and show average price of all printed proxies
- [ ] Implement "Export as.." on /ui/api/proxies
- [ ] Implement logging
- [ ] Implement remote logging
- [ ] Write dotenv.template
- [ ] Support PTCGL basic energy format (4 Basic {P} Energy SVE 5, 2 Basic {P} Energy CRZ 156)
- [ ] Properly support both PTCGL and PTCGO decklist formats
- [ ] Edit decklist hack using "history.back()" doesn't work reliably
- [ ] Support Shiny Vault cards (They seem to not have a standard set id?, some say they're part of the main set they
  belong to, some say they belong to their own set: sm1)
- [ ] BREAK and LEGEND cards don't work properly in text mode with illustrations enabled
- [ ] Text mode only supports 1 deck at a time (should support 3)
- [ ] Implement single click bookmarklet
- [ ] Set discord link on the changelog page
- [ ] Add todo/known issues page?
- [ ] Redesign features page?
- [ ] Make a database table for card issues so that the table can be automatically generated
- [ ] Make some kind of utility to add records to the above table (manage.py like program)
- [ ] Refactor all the text on the website that changed (such as links, email addrs, and changed features like "up to
  3 decklists")

## IP

- [~] Implement sentry support
- [~] Implement "generate from URL options"

## DONE

- [X] Implement some kind of bg job that runs on a timer to update the database
- [X] Make a background job that deletes expired shares
- [X] Convert the full list of set codes from a google sheet to a webpage with a table
- [X] Convert the missing cards from a google sheet to a webpage with a table
- [X] Make some kind of way to enable "maintenance mode" so that the main webserver only hosts the "under maintenance"
  page automatically

## MISSING CARDS:

- hsp-HGSS18
- xyp-XY39 doesn't have a high-res image
- xyp-XY46 doesn't have a high-res image
- xyp-XY68 doesn't have a high-res image
- ALL OF mcd14
- ALL OF mcd15
- ALL OF mcd17
- ALL OF mcd18

