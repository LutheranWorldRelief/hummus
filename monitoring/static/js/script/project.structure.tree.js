(function () {
    var app, deps;

    deps = ['treeGrid'];

    app = angular.module('treeGridStructure', deps)
            .service('DatosService', DatosService)
            .constant('UrlsAcciones', UrlsAcciones);
    app.controller('treeGridController', function ($scope, UrlsAcciones, DatosService, $timeout) {
        var tree;
        $scope.formulario = {};
        $scope.tree_data = {};



        $scope.cargarDatos = function () {
            DatosService
                    .Consultar(UrlsAcciones.UrlDatos, $scope.formulario)
                    .then(function (result) {
                        console.log($scope.formulario);
                        $scope.tree_data = getTree(result.data, 'id', 'structure_id');
                    })
                    .catch(function (mensaje, codigo) {
                        console.log(mensaje);
                    });
        };



        $scope.my_tree = tree = {};
        $scope.expanding_property = {
            field: "description",
            displayName: "Structure Description",
            sortable: true,
            filterable: true,
            cellTemplate: "<i>{{row.branch[expandingProperty.field]}}</i>"
        };
        $scope.col_defs = [
            {
                field: "code",
                sortable: true,
                displayName: "Code",
                sortingType: "string",
                filterable: true
            },
            {
                field: "notes",
                sortable: true,
                displayName: "Notes",
                sortingType: "string",
                filterable: true
            },
            {
                field: "id",
                displayName: " ",
                cellTemplate: "<a href='" + UrlsAcciones.UrlView + "?id={{row.branch[col.field]}}&project=" + UrlsAcciones.Proyecto + "'><i class='glyphicon glyphicon-pencil'></i></a>"
            },
            {
                field: "id",
                displayName: " ",
                cellTemplate: "<a href='" + UrlsAcciones.UrlCreate + "?project=" + UrlsAcciones.Proyecto + "&parent={{row.branch[col.field]}}'><i class='glyphicon glyphicon-plus'></i></a>"
            },
            {
                field: "id",
                displayName: " ",
                cellTemplate: "<a href='" + UrlsAcciones.UrlEliminar + "?id={{row.branch[col.field]}}&project=" + UrlsAcciones.Proyecto + "'><i class='glyphicon glyphicon-trash'></i></a>"
            }
        ];
        $scope.my_tree_handler = function (branch) {
            console.log('you clicked on', branch);
        };

        function getTree(data, primaryIdName, parentIdName) {
            if (!data || data.length == 0 || !primaryIdName || !parentIdName)
                return [];

            var tree = [],
                    rootIds = [],
                    item = data[0],
                    primaryKey = item[primaryIdName],
                    treeObjs = {},
                    parentId,
                    parent,
                    len = data.length,
                    i = 0;

            while (i < len) {
                item = data[i++];
                primaryKey = item[primaryIdName];
                treeObjs[primaryKey] = item;
                parentId = item[parentIdName];

                if (parentId) {
                    parent = treeObjs[parentId];

                    if (parent.children) {
                        parent.children.push(item);
                    } else {
                        parent.children = [item];
                    }
                } else {
                    rootIds.push(primaryKey);
                }
            }

            for (var i = 0; i < rootIds.length; i++) {
                tree.push(treeObjs[rootIds[i]]);
            }
            ;

            return tree;
        }

    });

}).call(this);
