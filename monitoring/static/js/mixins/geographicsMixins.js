var geographicsMixins = {
    data() {
        return {
            geojson: {
                type: "FeatureCollection",
                features: []
            },
            dataTableGeographic: [],
            map: null,
            info: null,
            customStyle: {
                fillColor: "#00aaa7",
                weight: 1,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7
            },
            actual_participants: 0,
            target_participants: 0,
        }
    },
    methods: {
        loadCountriesMaps() {
            if (this.map)
                this.map.remove();

            this.map = new L.Map('map');
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>'
            }).addTo(this.map);

            let info = L.control();

            info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info'); //div con clase 'info'
                this.update();
                return this._div;
            };

            info.update = function (props) {
                let title1 = gettext('Country');
                let title2 = gettext('Total');
                let title3 = gettext('Percentage');
                let title4 = gettext('Hover over a country');
                let text = '';
                if (props) {
                    text = `<b>${title1}: </b>${props.name}<br/><b>${title2}: </b>${props.total}<br/><b>${title3}: </b>${props.percentage}`
                } else {
                    text = `<b>${title4}</b>`;
                }
                this._div.innerHTML = text;
            };

            info.addTo(this.map);

            $.get(UrlsAcciones.UrlCountriesGeography, this.requestParameters)
                .then(response => {
                    let data = response;
                    this.dataTableGeographic = [];

                    this.actual_participants = 0;
                    this.target_participants = 0;
                    data.participants.forEach((country_data) => {
                        this.dataTableGeographic.push({
                            name: country_data.name,
                            total_participants: this.formatNumber(country_data.total),
                            total_target: this.formatNumber(country_data.total_target),
                            percentage_participants: country_data.percentage.toFixed(2),
                        });
                        this.actual_participants += country_data.total;
                        this.target_participants += country_data.total_target;
                    });

                    $.get(UrlsAcciones.UrlCountriesPolygons)
                        .then(response => {
                            let countries = response;
                            let geojSonLayerGroup = null;

                            this.geojson.features = [];
                            data.participants.forEach(participant => {

                                let country = countries.features.find(country => country.id === participant.alfa3);
                                country.properties.women = participant.women;
                                country.properties.men = participant.men;
                                country.properties.total = participant.total;
                                country.properties.percentage = `${participant.percentage.toFixed(2)} %`;
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
                                this.map.fitBounds(e.target.getBounds());
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
                                style: this.customStyle
                            });

                            geojSonLayerGroup.addTo(this.map);

                            /*Zoom automático*/
                            this.map.fitBounds(geojSonLayerGroup.getBounds());

                        });
                });
        },
        formatNumber(num) {
            return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
        }
    }
};