/* global _ */

/*
 * Complex scripted dashboard
 * This script generates a dashboard object that Grafana can load. It also takes a number of user
 * supplied URL parameters (in the ARGS variable)
 *
 * Return a dashboard object, or a function
 *
 * For async scripts, return a function, this function must take a single callback function as argument,
 * call this callback function with the dashboard object (look at scripted_async.js for an example)
 */


//Test

'use strict';

// accessible variables in this scope
var window, document, ARGS, $, jQuery, moment, kbn;

// Setup some variables
var dashboard;

dashboard = {
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 9,
  "links": [],
  "panels": [],
  "refresh": "1s",
  "schemaVersion": 16,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-30s",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": [
      "1s",
      "5s",
      "10s",
      "30s",
      "1m",
      "5m",
      "15m",
      "30m",
      "1h",
      "2h",
      "1d"
    ],
    "time_options": [
      "10s",
      "30s",
      "1m",
      "5m",
      "15m",
      "1h",
      "6h",
      "12h",
      "24h",
      "2d",
      "7d",
      "30d"
    ]
  },
  "timezone": "",
  "title": ARGS.measurement_name,
  "uid": "g00_ieRRz",
  "version": 3
};



var fields = ARGS.fields.split(',');
var fields_unit = ARGS.fieldsunit.split(',');
var measurement_select = [];
var measurement_description = "";

for (var i = 0; i < fields.length; i++) {
  var newfield = [
    {
      "params": [
        fields[i]
      ],
      "type": "field"
    }
  ];
  measurement_select.push(newfield);
  measurement_description += fields[i] + " in " + fields_unit[i] + "  \n";
}


// var measurement_select = [
//   [
//     {
//       "params": [
//         "pitch"
//       ],
//       "type": "field"
//     }
//   ],
//   [
//     {
//       "params": [
//         "roll"
//       ],
//       "type": "field"
//     }
//   ]
// ];


var tagkeys = ARGS.tagkeys.split(',');
var tagvalues = ARGS.tagvalues.split(',');
var measurement_tags = [];

for (var i = 0; i < tagkeys.length; i++) {
  var newtag = {
    "condition": "AND",
    "key": tagkeys[i],
    "operator": "=",
    "value": tagvalues[i]
  };
  measurement_tags.push(newtag);
}

// var measurement_tags = [
//   {
//     "condition": "AND",
//     "key": "device_name",
//     "operator": "=",
//     "value": "zpi1"
//   },
//   {
//     "condition": "AND",
//     "key": "service_name",
//     "operator": "=",
//     "value": "lagesensor"
//   },
//   {
//     "condition": "AND",
//     "key": "sensor",
//     "operator": "=",
//     "value": "mpu6050"
//   }
// ];







var measurement_panel = {
      "description": measurement_description,
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": null,
      "fill": 1,
      "gridPos": {
        "h": 10,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 2,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "percentage": false,
      "pointradius": 5,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "groupBy": [],
          "measurement": ARGS.measurement_influxdb_name,
          "orderByTime": "ASC",
          "policy": "default",
          "refId": "A",
          "resultFormat": "time_series",
          "select": measurement_select,
          "tags": measurement_tags
        }
      ],
      "thresholds": [],
      "timeFrom": null,
      "timeShift": null,
      "title": ARGS.measurement_name,
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "short",
          "label": fields_unit[0],
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    };


dashboard.panels.push(measurement_panel);

var mqtt_delay = {
  "aliasColors": {},
  "bars": false,
  "dashLength": 10,
  "dashes": false,
  "datasource": null,
  "fill": 1,
  "gridPos": {
    "h": 7,
    "w": 24,
    "x": 0,
    "y": 10
  },
  "id": 3,
  "legend": {
    "avg": false,
    "current": false,
    "max": false,
    "min": false,
    "show": true,
    "total": false,
    "values": false
  },
  "lines": true,
  "linewidth": 1,
  "links": [],
  "nullPointMode": "null",
  "percentage": false,
  "pointradius": 5,
  "points": false,
  "renderer": "flot",
  "seriesOverrides": [],
  "spaceLength": 10,
  "stack": false,
  "steppedLine": false,
  "targets": [
    {
      "groupBy": [],
      "measurement": "lage",
      "orderByTime": "ASC",
      "policy": "default",
      "refId": "A",
      "resultFormat": "time_series",
      "select": [
        [
          {
            "params": [
              "delay_received_msvalue"
            ],
            "type": "field"
          }
        ]
      ],
      "tags": [
        {
          "key": "device_name",
          "operator": "=",
          "value": "zpi1"
        },
        {
          "condition": "AND",
          "key": "service_name",
          "operator": "=",
          "value": "lagesensor"
        },
        {
          "condition": "AND",
          "key": "sensor",
          "operator": "=",
          "value": "mpu6050"
        }
      ]
    }
  ],
  "thresholds": [],
  "timeFrom": null,
  "timeShift": null,
  "title": "MQTT Delay/ms",
  "tooltip": {
    "shared": true,
    "sort": 0,
    "value_type": "individual"
  },
  "type": "graph",
  "xaxis": {
    "buckets": null,
    "mode": "time",
    "name": null,
    "show": true,
    "values": []
  },
  "yaxes": [
    {
      "format": "ms",
      "label": null,
      "logBase": 1,
      "max": null,
      "min": null,
      "show": true
    },
    {
      "format": "short",
      "label": null,
      "logBase": 1,
      "max": null,
      "min": null,
      "show": true
    }
  ],
  "yaxis": {
    "align": false,
    "alignLevel": null
  }
};

dashboard.panels.push(mqtt_delay);

// // All url parameters are available via the ARGS object
// var ARGS;

// // Initialize a skeleton with nothing but a rows array and service object
// dashboard = {
//   rows : [],
// };

// // Set a title
// // dashboard.title = 'Scripted dash';

// // Set default time
// // time can be overridden in the url using from/to parameters, but this is
// // handled automatically in grafana core during dashboard initialization
// dashboard.time = {
//   from: "now-30s",
//   to: "now"
// };

// var rows = 1;
// var seriesName = 'argName';

// // if(!_.isUndefined(ARGS.rows)) {
// //   rows = parseInt(ARGS.rows, 10);
// // }

// // if(!_.isUndefined(ARGS.name)) {
// //   seriesName = ARGS.name;
// // }

// // for (var i = 0; i < rows; i++) {

// //   dashboard.rows.push({
// //     title: 'Chart',
// //     height: '300px',
// //     panels: [
// //       {
// //         title: 'Events',
// //         type: 'graph',
// //         span: 12,
// //         fill: 1,
// //         linewidth: 2,
// //         targets: [
// //           {
// //             'target': "randomWalk('" + seriesName + "')"
// //           },
// //           {
// //             'target': "randomWalk('random walk2')"
// //           }
// //         ],
// //         seriesOverrides: [
// //           {
// //             alias: '/random/',
// //             yaxis: 2,
// //             fill: 0,
// //             linewidth: 5
// //           }
// //         ],
// //         tooltip: {
// //           shared: true
// //         }
// //       }
// //     ]
// //   });
// // }

// // if(!_.isUndefined(ARGS.measurement_influxdb_name)) {
// //   dashboard.title = ARGS.measurement_influxdb_name;
// // }

// dashboard.title = ARGS.measurement_influxdb_name;

// dashboard.rows.push({
//   title: ARGS.measurement_influxdb_name,
//   height: '300px',
//   panels: [
//     {
//       "aliasColors": {},
//       "bars": false,
//       "dashLength": 10,
//       "dashes": false,
//       "datasource": null,
//       "fill": 1,
//       "gridPos": {
//         "h": 10,
//         "w": 24,
//         "x": 0,
//         "y": 0
//       },
//       "id": 2,
//       "legend": {
//         "avg": false,
//         "current": false,
//         "max": false,
//         "min": false,
//         "show": true,
//         "total": false,
//         "values": false
//       },
//       "lines": true,
//       "linewidth": 1,
//       "nullPointMode": "null",
//       "percentage": false,
//       "pointradius": 5,
//       "points": false,
//       "renderer": "flot",
//       "seriesOverrides": [],
//       "spaceLength": 10,
//       "stack": false,
//       "steppedLine": false,
//       "targets": [
//         {
//           "groupBy": [],
//           "measurement": "lage",
//           "orderByTime": "ASC",
//           "policy": "default",
//           "refId": "A",
//           "resultFormat": "time_series",
//           "select": [
//             [
//               {
//                 "params": [
//                   "pitch"
//                 ],
//                 "type": "field"
//               }
//             ],
//             [
//               {
//                 "params": [
//                   "roll"
//                 ],
//                 "type": "field"
//               }
//             ]
//           ],
//           "tags": [
//             {
//               "key": "device_name",
//               "operator": "=",
//               "value": "zpi1"
//             },
//             {
//               "condition": "AND",
//               "key": "service_name",
//               "operator": "=",
//               "value": "lagesensor"
//             },
//             {
//               "condition": "AND",
//               "key": "sensor",
//               "operator": "=",
//               "value": "mpu6050"
//             }
//           ]
//         }
//       ],
//       "thresholds": [],
//       "timeFrom": null,
//       "timeShift": null,
//       "title": "Panel Title",
//       "tooltip": {
//         "shared": true,
//         "sort": 0,
//         "value_type": "individual"
//       },
//       "type": "graph",
//       "xaxis": {
//         "buckets": null,
//         "mode": "time",
//         "name": null,
//         "show": true,
//         "values": []
//       },
//       "yaxes": [
//         {
//           "format": "short",
//           "label": null,
//           "logBase": 1,
//           "max": null,
//           "min": null,
//           "show": true
//         },
//         {
//           "format": "short",
//           "label": null,
//           "logBase": 1,
//           "max": null,
//           "min": null,
//           "show": true
//         }
//       ],
//       "yaxis": {
//         "align": false,
//         "alignLevel": null
//       }
//     },
//     {
//       "aliasColors": {},
//       "bars": false,
//       "dashLength": 10,
//       "dashes": false,
//       "datasource": null,
//       "fill": 1,
//       "gridPos": {
//         "h": 7,
//         "w": 24,
//         "x": 0,
//         "y": 10
//       },
//       "id": 3,
//       "legend": {
//         "avg": false,
//         "current": false,
//         "max": false,
//         "min": false,
//         "show": true,
//         "total": false,
//         "values": false
//       },
//       "lines": true,
//       "linewidth": 1,
//       "links": [],
//       "nullPointMode": "null",
//       "percentage": false,
//       "pointradius": 5,
//       "points": false,
//       "renderer": "flot",
//       "seriesOverrides": [],
//       "spaceLength": 10,
//       "stack": false,
//       "steppedLine": false,
//       "targets": [
//         {
//           "groupBy": [],
//           "measurement": "lage",
//           "orderByTime": "ASC",
//           "policy": "default",
//           "refId": "A",
//           "resultFormat": "time_series",
//           "select": [
//             [
//               {
//                 "params": [
//                   "delay_received_msvalue"
//                 ],
//                 "type": "field"
//               }
//             ]
//           ],
//           "tags": [
//             {
//               "key": "device_name",
//               "operator": "=",
//               "value": "zpi1"
//             },
//             {
//               "condition": "AND",
//               "key": "service_name",
//               "operator": "=",
//               "value": "lagesensor"
//             },
//             {
//               "condition": "AND",
//               "key": "sensor",
//               "operator": "=",
//               "value": "mpu6050"
//             }
//           ]
//         }
//       ],
//       "thresholds": [],
//       "timeFrom": null,
//       "timeShift": null,
//       "title": "MQTT Delay/ms",
//       "tooltip": {
//         "shared": true,
//         "sort": 0,
//         "value_type": "individual"
//       },
//       "type": "graph",
//       "xaxis": {
//         "buckets": null,
//         "mode": "time",
//         "name": null,
//         "show": true,
//         "values": []
//       },
//       "yaxes": [
//         {
//           "format": "ms",
//           "label": null,
//           "logBase": 1,
//           "max": null,
//           "min": null,
//           "show": true
//         },
//         {
//           "format": "short",
//           "label": null,
//           "logBase": 1,
//           "max": null,
//           "min": null,
//           "show": true
//         }
//       ],
//       "yaxis": {
//         "align": false,
//         "alignLevel": null
//       }
//     }
//   ]
// });


return dashboard;
