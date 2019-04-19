var countTo = angular.module('countTo', [])
    .directive('countTo', ['$timeout', function ($timeout) {
        return {
            replace: false,
            scope: true,
            link: function (scope, element, attrs) {

                var e = element[0];
                var num, refreshInterval, duration, steps, step, countTo, value, increment;

                var webify = function (k) {
                    var n = 0;
                    var t_n = 0;
                    if ((Math.pow(10, 6) > k ) && (k > Math.pow(10, 4))) {
                        n = Math.floor(k / Math.pow(10, 3)).toString().concat('K');
                    }
                    else if ((Math.pow(10, 9) > k) && (k > Math.pow(10, 6))) {
                        t_n = (k / Math.pow(10, 6));
                        t_n = +t_n.toFixed(2);
                        n = t_n.toString().concat('M');
                    }
                    else if ((Math.pow(10, 12) > k) && (k > Math.pow(10, 9))) {
                        t_n = (k / Math.pow(10, 9));
                        t_n = +t_n.toFixed(2);
                        n = t_n.toString().concat('B');
                    }
                    else if (k <= Math.pow(10, 4)) {
                        n = Math.floor(k).toString();
                    }
                    return n
                };

                var calculate = function () {
                    refreshInterval = 30;
                    step = 0;
                    scope.timoutId = null;
                    countTo = parseInt(attrs.countTo) || 0;
                    scope.value = parseInt(attrs.value, 10) || 0;
                    duration = (parseFloat(attrs.duration) * 1000) || 0;

                    steps = Math.ceil(duration / refreshInterval);
                    increment = ((countTo - scope.value) / steps);
                    num = scope.value;
                };

                var tick = function () {
                    scope.timoutId = $timeout(function () {
                        num += increment;
                        step++;
                        if (step >= steps) {
                            $timeout.cancel(scope.timoutId);
                            num = countTo;
                            e.textContent = webify(countTo);
                        } else {
                            e.textContent = webify(Math.round(num));
                            tick();
                        }
                    }, refreshInterval);

                };

                var start = function () {
                    if (scope.timoutId) {
                        $timeout.cancel(scope.timoutId);
                    }
                    calculate();
                    tick();
                };

                attrs.$observe('countTo', function (val) {
                    if (val) {
                        start();
                    }
                });

                //noinspection JSUnusedLocalSymbols
                attrs.$observe('value', function (val) {
                    start();
                });

                return true;
            }
        }

    }]);
