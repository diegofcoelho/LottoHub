/**
 * Created by dfcoelho on 09/06/2017.
 */
(function () {
    'use strict';
    angular.module('plotly', []).directive('plotly', ['$compile', '$templateCache', '$window',
        function ($compile, $templateCache, $window) {
            var default_template = '<div class="plotly-grid""></div>';
            return {
                restrict: 'E',
                /* id="myDiv" style="min-height: 80vh; min-width: 98vw;" layout="column" layout-align="center center" */
                scope: {
                    plotlyData: '=',
                    plotlyLayout: '=',
                    plotlyOptions: '=',
                    plotlyEvents: '=',
                    plotlyManualDataUpdate: '=',
                    plotlyFull: '='
                },
                template: default_template,
                link: function (scope, element) {
                    if (scope.plotlyFull || false) {
                        default_template = '<div class="plotly-full"></div>';
                        element.html(default_template);
                        $compile(element.contents())(scope);
                    }
                    var graph = element[0].children[0];
                    //var graph = document.getElementById("myDiv");
                    var initialized = false;

                    function subscribeToEvents(graph) {
                        scope.plotlyEvents(graph);
                    }

                    function onUpdate() {
                        //No data yet, or clearing out old data
                        if (!(scope.plotlyData)) {
                            if (initialized) {
                                Plotly.Plots.purge(graph);
                                graph.innerHTML = '';
                            }
                            return;
                        }
                        //If this is the first run with data, initialize
                        if (!initialized) {
                            initialized = true;
                            Plotly.newPlot(graph, scope.plotlyData, scope.plotlyLayout, scope.plotlyOptions);
                            if (scope.plotlyEvents) {
                                subscribeToEvents(graph);
                            }
                        }
                        graph.layout = scope.plotlyLayout;
                        graph.data = scope.plotlyData;
                        Plotly.redraw(graph);
                        Plotly.Plots.resize(graph);
                    }

                    function onResize() {
                        if (!(initialized && scope.plotlyData)) return;
                        Plotly.Plots.resize(graph);
                    }

                    scope.$watch(
                        function (scope) {
                            return scope.plotlyLayout;
                        },
                        function (newValue, oldValue) {
                            if (angular.equals(newValue, oldValue) && initialized) return;
                            onUpdate();
                        }, true);

                    if (!scope.plotlyManualDataUpdate) {
                        scope.$watch(
                            function (scope) {
                                return scope.plotlyData;
                            },
                            function (newValue, oldValue) {
                                if (angular.equals(newValue, oldValue) && initialized) return;
                                onUpdate();
                            }, true);
                    }

                    /**
                     * Listens to 'tracesUpdated' event broadcasted from controller to update plot.
                     */

                    scope.$on('tracesUpdated', function () {
                        onUpdate();
                    });

                    scope.$watch(function () {
                        return {
                            'h': graph.offsetHeight,
                            'w': graph.offsetWidth
                        };
                    }, function (newValue, oldValue) {
                        if (angular.equals(newValue, oldValue)) return;
                        onResize();
                    }, true);

                    angular.element($window).bind('resize', onResize);

                }
            };
        }
    ]);
})();
