from flask import render_template


def make_invalid_dl_error(dl):
    return render_template("errors/error.html",
                           errors=[
                               f"Something is wrong with your decklist. Please check your decklist and try again. If you're still having issues, check the help page, or contact me (contact info on help page) (Provided list: '{dl}')"],
                           meta={"title": "Error", "description": "Something went wrong along the way"})
