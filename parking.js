const scrapeIt = require("scrape-it");
const moment = require('moment-timezone');
const _ = require('lodash');
const util = require('util')

const dateRegEx = new RegExp(/: (.*)/);

function cleanUp(page) {
    var ignore = ['Station', 'Parking Status'];

    var names =  [
         'North Springs'
       , 'Sandy Springs'
       , 'Dunwoody'
       , 'Doraville'
       , 'Chamblee'
       , 'Brookhaven'
       , 'Lenox'
       , 'Lindbergh Center'
       , 'College Park'
       , 'Kensington' ];

    stations = [];
    for (i = 0; i < page.rows.length - 1; i++) {
      row = page.rows[i];
      if (_.includes(ignore, row)) {
          // do nothing
      } else if (_.includes(names, row)) {
          stations.push({
              name: row
            , lots: []
          });
      } else {
          var lots = _.last(stations).lots
          if (_.includes(_.toLower(row), 'open')) {
              lots.push({
                  status: 'open'
                , label: row
              })
          } else if (_.includes(_.toLower(row), 'full')) {
              lots.push({
                  status: 'full'
                , label: row
              })
          } else {
            // do nothing
          }
      }
    }

    var api = {
        lastUpdated: page.lastUpdated
      , stations: stations
    };

    return api;
}

// Callback interface
scrapeIt("http://www.itsmarta.com/parking.aspx", {

    lastUpdated: {
        selector: "div.l-main > div > div > p:nth-child(2)"
      , convert: function(x) {
          var str = x.match(dateRegEx)[1].trim().replace(/\s+/g,' ');
          return moment.tz(str, 'M/DD/YYYY h:mmA', "America/New_York").toLocaleString();
        }
    },
    rows: {
        listItem: "#ctl00_ContentPlaceHolder1_cntpolice > div > div > div > div > table:nth-child(5) > tbody > tr > td"
      , convert: function(x) {
        return x.trim();
      }
    }

}, (err, page) => {
    var output = cleanUp(page);
    console.log(util.inspect(output, false, null))
});
