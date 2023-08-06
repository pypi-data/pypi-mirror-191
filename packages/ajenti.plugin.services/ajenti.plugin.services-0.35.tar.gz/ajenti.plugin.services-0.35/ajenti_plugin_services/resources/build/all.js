'use strict';

angular.module('ajenti.services', ['core']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/services', {
        templateUrl: '/services:resources/partial/index.html',
        controller: 'ServicesIndexController'
    });

    $routeProvider.when('/view/services/:managerId', {
        templateUrl: '/services:resources/partial/index.html',
        controller: 'ServicesIndexController'
    });
});


'use strict';

angular.module('ajenti.services').controller('ServicesIndexController', function ($scope, $routeParams, $uibModal, notify, pageTitle, services, gettext) {
    pageTitle.set(gettext('Services'));

    $scope.services = [];
    $scope.titles = {
        'stop': gettext("Stop service"),
        'start': gettext("Start service"),
        'restart': gettext("Restart service"),
        'kill': gettext("Kill service"),
        'enable': gettext("Enable service"),
        'disable': gettext("Disable service")
    };

    services.getManagers().then(function (managers) {
        $scope.managers = managers;

        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = $scope.managers[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                var manager = _step.value;

                if ($routeParams.managerId && manager.id !== $routeParams.managerId) {
                    continue;
                }
                services.getServices(manager.id).then(function (services) {
                    var _iteratorNormalCompletion2 = true;
                    var _didIteratorError2 = false;
                    var _iteratorError2 = undefined;

                    try {
                        for (var _iterator2 = services[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                            var service = _step2.value;

                            $scope.services.push(service);
                        }
                    } catch (err) {
                        _didIteratorError2 = true;
                        _iteratorError2 = err;
                    } finally {
                        try {
                            if (!_iteratorNormalCompletion2 && _iterator2.return) {
                                _iterator2.return();
                            }
                        } finally {
                            if (_didIteratorError2) {
                                throw _iteratorError2;
                            }
                        }
                    }
                });
            }
        } catch (err) {
            _didIteratorError = true;
            _iteratorError = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion && _iterator.return) {
                    _iterator.return();
                }
            } finally {
                if (_didIteratorError) {
                    throw _iteratorError;
                }
            }
        }
    });

    $scope.showStatus = function (service) {
        services.getStatus(service.managerId, service.id).then(function (data) {
            $scope.status = data;
            $uibModal.open({
                templateUrl: '/services:resources/partial/systemd_status.modal.html',
                controller: 'SystemdStatusModalController',
                size: 'lg',
                resolve: {
                    service: function service() {
                        return $scope.service;
                    },
                    status: function status() {
                        return $scope.status;
                    }
                }
            });
        });
    };

    $scope.closeStatus = function () {
        $scope.showDialog = false;
        $scope.selectedService = "";
    };

    $scope.runOperation = function (service, operation) {
        return services.runOperation(service, operation).then(function () {
            return services.getService(service.managerId, service.id).then(function (data) {
                angular.copy(data, service);
                return notify.success(gettext('Done'));
            });
        }).catch(function (err) {
            return notify.error(gettext('Service operation failed'), err.message);
        });
    };
});

angular.module('ajenti.services').controller('SystemdStatusModalController', function ($scope, $uibModalInstance, gettext, notify, service, status) {

    $scope.service = service;
    $scope.status = status;

    $scope.close = function () {
        return $uibModalInstance.close();
    };
});


'use strict';

angular.module('ajenti.services').controller('ServiceWidgetController', function ($scope, services, notify, gettext) {
    $scope.$on('widget-update', function ($event, id, data) {
        if (id !== $scope.widget.id) {
            return;
        }
        $scope.service = data;
    });

    $scope.runOperation = function (o) {
        var svc = {
            managerId: $scope.widget.config.manager_id,
            id: $scope.widget.config.service_id
        };
        services.runOperation(svc, o).catch(function (e) {
            return notify.error(gettext('Service operation failed'), e.message);
        });
    };
});

angular.module('ajenti.services').controller('ServiceWidgetConfigController', function ($scope, services) {
    $scope.services = [];

    services.getManagers().then(function (managers) {
        $scope.managers = managers;

        $scope.managers.forEach(function (manager) {
            return services.getServices(manager.id).then(function (services) {
                return services.map(function (service) {
                    return $scope.services.push(service);
                });
            });
        });
    });
});


'use strict';

angular.module('ajenti.services').service('services', function ($http) {
    this.getManagers = function () {
        return $http.get("/api/services/managers").then(function (response) {
            return response.data;
        });
    };

    this.getServices = function (managerId) {
        return $http.get('/api/services/manager/' + managerId).then(function (response) {
            return response.data;
        });
    };

    this.getStatus = function (managerId, serviceId) {
        return $http.get('/api/services/status/' + managerId + '/' + serviceId).then(function (response) {
            return response.data;
        });
    };

    this.getService = function (managerId, serviceId) {
        return $http.get('/api/services/manager/' + managerId + '/' + serviceId).then(function (response) {
            return response.data;
        });
    };

    this.runOperation = function (service, operation) {
        return $http.post('/api/services/do/' + operation + '/' + service.managerId + '/' + service.id).then(function (response) {
            return response.data;
        });
    };

    return this;
});


