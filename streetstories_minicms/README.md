# Mini-CMS for Street Stories made at Canvas media innovation hackathon

## Files

- Combined with `spreadsheets2csv` in parent directory, you can generate JS code for the Street Stories platform using a Google Sheets document with two worksheets, one for slides and the other for places.
- `spreadsheets2csv` assumes that you have a valid OAuth token... see in parent directory on how to get it
- `merge.py` parses the two CSV files generated from your Sheets into a JS file for use with Street Stories (ours is called `hongkong.js`)
- `call.sh`: the file that wraps all the other scripts and where you should replace the values at the top with your own
  - Use `spreadsheetdata.py` (also in parent dir) with your Sheets key to find out the worksheet ids
  - Because we use a really basic `sed` to convert strings to numbers and variable names in the JS file that doesn't check empty strings, you should make sure you fill the `lat`, `lng`, `heading`, `infotype` and `type` in your Sheets or it'll break :(
- You would still have to manually customize `content.json` for your first slide and sounds
- We left most of our contents files
- Our `main.js` is slightly modified to accomodate our video delivery system (Vidly) and assumes you have a subdir called img/pics where all the photos go

## Links

- Link to the Street Stories project (not by us): http://canvas.challengepost.com/submissions/30704-street-stories
- Implementation by South China Morning Post for Umbrella Revolution (by us): http://www.scmp.com/news/hong-kong/article/1659355/multimedia-tracing-moments-occupy-hong-kongs-streets
- Example of our Google Sheets: https://docs.google.com/spreadsheets/d/1ure7af4zsHwJSU\_DAH7Cdx9J26mf1c1n9mb\_BSDXdFI/edit?usp=sharing
