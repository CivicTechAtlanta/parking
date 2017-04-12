const scrapeIt = require("scrape-it");
const moment = require('moment-timezone');

const dateRegEx = new RegExp(/: (.*)/);

// Callback interface
scrapeIt("http://www.itsmarta.com/parking.aspx", {

    lastUpdated: {
        selector: "div.l-main > div > div > p:nth-child(2)"
      , convert: function(x) {
          var str = x.match(dateRegEx)[1].trim().replace(/\s+/g,' ');
          return moment.tz(str, 'M/DD/YYYY h:mmA', "America/New_York").toLocaleString();
        }
    },
    stations: {
        // Possible change to reduce breakage: get closer using existing class='introduction' on div surrounding table tag.
        listItem: "#ctl00_ContentPlaceHolder1_cntpolice > div > div > div > div > table:nth-child(5) > tbody > tr > td"
      , convert: function(x) {
        return x.trim();
      }
    }

}, (err, page) => {
    console.log(err || page);
});
