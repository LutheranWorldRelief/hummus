var geographicsMixins = {
    data() {
        return {
            showing_map: false,
            geojson: {
                type: "FeatureCollection",
                features: []
            },
            dataTableGeographic: [],
        }
    },
    methods: {
        loadCountriesMaps() {

            let map = new L.Map('map');
            let info = L.control();
            let customStyle = {
                fillColor: "#00aaa7",
                weight: 1,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7
            };

            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>'
            }).addTo(map);

            info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info'); //div con clase 'info'
                this.update();
                return this._div;
            };

            info.update = function (props) {
                let title1 = gettext('Participants');
                let title2 = gettext('Country');
                let title3 = gettext('Total');
                let title4 = gettext('Percentage');
                let title5 = gettext('Hover over a country');
                this._div.innerHTML = `<h4>${title1}</h4>`;
                if (props) {
                    this._div.innerHTML += `<b>${title2}: </b>${props.name}<br/><b>${title3}: </b>${props.total}<br/><b>${title4}: </b>${props.percentage}`
                } else {
                    this._div.innerHTML += `<b>${title5}</b>`;
                }
            };

            info.addTo(map);

            $.get(UrlsAcciones.UrlCountriesGeography, this.requestParameters)
                .then(response => {
                    let data = response;

                    data.participants.forEach((country_data) => {
                        this.dataTableGeographic.push({
                            name: country_data.name,
                            total_participants: country_data.total,
                            percentage_participants: country_data.percentage,
                        })
                    });

                    $.get(UrlsAcciones.UrlCountriesPolygons)
                        .then(response => {
                            let countries = response;
                            let geojSonLayerGroup;

                            data.participants.forEach(participant => {
                                let country = countries.features.find(country => country.id === participant.alfa3);
                                country.properties.women = participant.women;
                                country.properties.men = participant.men;
                                country.properties.total = participant.total;
                                country.properties.percentage = `${Math.floor(participant.percentage)} %`;

                                this.geojson.features.push(country);
                            });

                            function highlightFeature(e) {
                                let layer = e.target;

                                layer.setStyle({
                                    weight: 1,
                                    color: '#666',
                                    dashArray: '',
                                    fillOpacity: 0.7
                                });

                                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                                    layer.bringToFront();
                                }

                                info.update(layer.feature.properties);
                            }

                            function resetHighlight(e) {
                                geojSonLayerGroup.resetStyle(e.target);
                                info.update();
                            }

                            function zoomToFeature(e) {
                                map.fitBounds(e.target.getBounds());
                            }

                            function onEachFeature(feature, layer) {
                                layer.on({
                                    mouseover: highlightFeature,
                                    mouseout: resetHighlight,
                                    click: zoomToFeature
                                });
                            }

                            geojSonLayerGroup = L.geoJson(this.geojson, {
                                onEachFeature: onEachFeature,
                                style: customStyle
                            });

                            geojSonLayerGroup.addTo(map);

                            /*Zoom automático*/
                            map.fitBounds(geojSonLayerGroup.getBounds());

                        });
                });
        }
    }

};