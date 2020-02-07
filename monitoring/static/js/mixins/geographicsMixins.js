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
            countries_polygons_json: {},
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
                let title2 = gettext('Participants');
                let title3 = gettext('Percentage');
                let title4 = gettext('Hover over a country');
                let title5 = gettext('Projects');
                let title6 = gettext('Subprojects');
                let text = '';
                if (props) {
                    text = `<b>${title1}: </b>${props.name}<br/><b>${title2}: </b>${props.total}`;
                    text += `<br><b>${title5}: </b>${props.projects}<br/><b>${title6}: </b>${props.subprojects}<br/>`;
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

                    data.participants.forEach((country_data) => {
                        let country = this.setCountryObjectZeros(country_data.name);

                        this.dataTableGeographic.push({
                            id: country_data.id,
                            flag_url: `https://www.countryflags.io/${country_data.id}/flat/16.png`,
                            name: country_data.name,
                            total_participants: country_data.total,
                            total_target: country_data.total_target,
                            percentage_participants: country_data.percentage.toFixed(2),
                            projects: country.projects,
                            subprojects: country.subprojects,
                        });
                    });


                    let countries = this.countries_polygons_json;
                    let geojSonLayerGroup = null;

                    this.geojson.features = [];
                    data.participants.forEach(participant => {
                        let data = this.setCountryObjectZeros(participant.name);

                        let country = countries.features.find(country => country.id === participant.alfa3);
                        country.properties.women = participant.women;
                        country.properties.men = participant.men;
                        country.properties.total = this.formatNumber(participant.total);
                        country.properties.percentage = `${participant.percentage.toFixed(2)} %`;
                        country.properties.projects = data.projects;
                        country.properties.subprojects = data.subprojects;
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
        },
        formatNumber(num) {
            return num.toLocaleString();
        },
        Sum(array, field_name) {
            let total = 0;
            for (const object of array) {
                total += object[field_name];
            }

            return this.formatNumber(total);
        },
        setCountryObjectZeros(country_name) {
            let object = {projects: 0, subprojects: 0};
            let data = this.list_countries.find((item) => {
                return item.name === country_name;
            });

            return this.empty(data) ? object : data;
        }
    }
};