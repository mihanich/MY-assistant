var config = {
  modules: [
              {
                      module: "alert",
              },
              {
                      module: "MMM-GoogleAssistant",
                      position: "top_right",
                      config: {
                              maxWidth: "100%",
                              header: "",
                              publishKey: 'pub-c-ac6c7193-78ed-463e-ab10-1c4a9212af65',
                              subscribeKey: 'sub-c-284a80f8-1730-11e9-b4a6-026d6924b094',
                              updateDelay: 500
                              }
              },
              {
                      module: "MMM-GoogleMapsTraffic",
                      position: "bottom_right",
                      config: {
                          key: "AIzaSyCGjDLrHAzwd2EMBT4sRjHf5m45qXobJ-U",
                          lat: 48.624804,
                          lng: 22.284832,
                          zoom: 15,
                          height: "500px",
                          width: "500px",
                          styledMapType: "night",
                          disableDefaultUI: true,
                          backgroundColor: "hsla(0, 0%, 0%, 0)",
                          markers: [
                                {
                                    lat: 48.6209024,
                                    lng: 22.2987616,
                                    fillColor: "red"
                                },
                                {
                                    lat: 48.6288806,
                                    lng: 22.2719127,
                                    fillColor: "yellow"
                                },
                            ],
                  },
              },

}
