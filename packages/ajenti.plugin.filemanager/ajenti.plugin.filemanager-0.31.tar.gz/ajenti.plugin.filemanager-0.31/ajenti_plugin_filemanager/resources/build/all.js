'use strict';

angular.module('ajenti.filemanager', ['core', 'flow', 'ajenti.filesystem']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/filemanager', {
        templateUrl: '/filemanager:resources/partial/index.html',
        controller: 'FileManagerIndexController'
    });

    $routeProvider.when('/view/filemanager/properties/:path*', {
        templateUrl: '/filemanager:resources/partial/properties.html',
        controller: 'FileManagerPropertiesController'
    });

    return $routeProvider.when('/view/filemanager/:path*', {
        templateUrl: '/filemanager:resources/partial/index.html',
        controller: 'FileManagerIndexController'
    });
});


'use strict';

angular.module('ajenti.filemanager').controller('FileManagerIndexController', function ($scope, $routeParams, $location, $localStorage, $timeout, notify, identity, filesystem, pageTitle, urlPrefix, tasks, messagebox, gettext) {
    pageTitle.set('path', $scope);
    $scope.loading = false;
    $scope.newDirectoryDialogVisible = false;
    $scope.newFileDialogVisible = false;
    $scope.clipboardVisible = false;
    $scope.uploadDialogVisible = false;

    $scope.load = function (path) {
        $scope.loading = true;
        $scope.splitted_path_items = path.split('/');
        $scope.splitted_path = [];
        progressive_path = '';
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = $scope.splitted_path_items[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                item = _step.value;

                if (item != '') {
                    progressive_path = progressive_path + '/' + item;
                    $scope.splitted_path.push({ 'path': progressive_path, 'name': item });
                }
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

        return filesystem.list(path).then(function (data) {
            $scope.path = path;
            $scope.items = data.items;
            $scope.parent = data.parent;
        }, function (data) {
            notify.error(gettext('Could not load directory'), data.message);
        }).finally(function () {
            $scope.loading = false;
        });
    };

    $scope.refresh = function () {
        return $scope.load($scope.path);
    };

    $scope.$on('push:filesystem', function ($event, msg) {
        if (msg === 'refresh') {
            $scope.refresh();
        }
    });

    $scope.navigate = function (path) {
        return $location.path(urlPrefix + '/view/filemanager/' + path);
    };

    $scope.select = function (item) {
        if (item.isDir) {
            $scope.navigate(item.path);
        } else {
            if ($scope.mode === 'open') {
                $scope.onSelect({ item: item });
            }
            if ($scope.mode === 'save') {
                $scope.name = item.name;
            }
        }
    };

    $scope.clearSelection = function () {
        $scope.items.forEach(function (item) {
            return item.selected = false;
        });
    };

    $localStorage.fileManagerClipboard = $localStorage.fileManagerClipboard || [];
    $scope.clipboard = $localStorage.fileManagerClipboard;

    $scope.showClipboard = function () {
        return $scope.clipboardVisible = true;
    };

    $scope.hideClipboard = function () {
        return $scope.clipboardVisible = false;
    };

    $scope.clearClipboard = function () {
        $scope.clipboard.length = 0;
        $scope.hideClipboard();
    };

    $scope.rename = function (item) {
        messagebox.prompt(gettext('New name')).then(function (msg) {
            if (!msg.value) {
                return;
            }
            dst = $scope.path + '/' + msg.value;
            filesystem.rename(item.path, dst).then(function (resp) {
                if (!resp.data) {
                    notify.error(gettext("File or directory already exists"));
                    return;
                }
                item.name = msg.value;
                item.path = dst;
            });
        });
    };

    $scope.doCut = function () {
        var _iteratorNormalCompletion2 = true;
        var _didIteratorError2 = false;
        var _iteratorError2 = undefined;

        try {
            for (var _iterator2 = $scope.items[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                var _item = _step2.value;

                if (_item.selected) {
                    $scope.clipboard.push({
                        mode: 'move',
                        item: _item
                    });
                }
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

        $scope.clearSelection();
    };

    $scope.doCopy = function () {
        var _iteratorNormalCompletion3 = true;
        var _didIteratorError3 = false;
        var _iteratorError3 = undefined;

        try {
            for (var _iterator3 = $scope.items[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
                var _item2 = _step3.value;

                if (_item2.selected) {
                    $scope.clipboard.push({
                        mode: 'copy',
                        item: _item2
                    });
                }
            }
        } catch (err) {
            _didIteratorError3 = true;
            _iteratorError3 = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion3 && _iterator3.return) {
                    _iterator3.return();
                }
            } finally {
                if (_didIteratorError3) {
                    throw _iteratorError3;
                }
            }
        }

        $scope.clearSelection();
    };

    $scope.doDelete = function () {
        return messagebox.show({
            text: gettext('Delete selected items?'),
            positive: gettext('Delete'),
            negative: gettext('Cancel')
        }).then(function () {
            var items = $scope.items.filter(function (item) {
                return item.selected;
            });
            tasks.start('aj.plugins.filesystem.tasks.Delete', [], { items: items });
            $scope.clearSelection();
        });
    };

    $scope.doPaste = function () {
        var items = angular.copy($scope.clipboard);
        tasks.start('aj.plugins.filesystem.tasks.Transfer', [], { destination: $scope.path, items: items }).then(function () {
            $scope.clearClipboard();
        });
    };

    // new file dialog

    $scope.showNewFileDialog = function () {
        $scope.newFileName = '';
        $scope.newFileDialogVisible = true;
    };

    $scope.doCreateFile = function () {
        if (!$scope.newFileName) {
            return;
        }

        return filesystem.createFile($scope.path + '/' + $scope.newFileName).then(function () {
            $scope.refresh();
            $scope.newFileDialogVisible = false;
        }, function (err) {
            notify.error(gettext('Could not create file'), err.data.message);
        });
    };

    // new directory dialog

    $scope.showNewDirectoryDialog = function () {
        $scope.newDirectoryName = '';
        $scope.newDirectoryDialogVisible = true;
    };

    $scope.doCreateDirectory = function () {
        if (!$scope.newDirectoryName) {
            return;
        }

        return filesystem.createDirectory($scope.path + '/' + $scope.newDirectoryName).then(function () {
            $scope.refresh();
            $scope.newDirectoryDialogVisible = false;
        }, function (err) {
            notify.error(gettext('Could not create directory'), err.data.message);
        });
    };

    $scope.onUploadBegin = async function ($flow) {
        $scope.uploadDialogVisible = true;
        filesystem.startFlowUpload($flow, $scope.path).then(function () {
            notify.success(gettext('Uploaded'));
            $scope.refresh();
            $scope.uploadDialogVisible = false;
        }, null, function (progress) {
            console.log(progress);
            $scope.uploadProgress = progress.sort(function (a, b) {
                a.name > b.name;
            });
        });
    };

    // ---

    identity.promise.then(function () {
        var root = identity.profile.fs_root || '/';
        var path = $routeParams.path || '/';
        if (path.indexOf(root) !== 0) {
            path = root;
        }

        if ($routeParams.path) {
            $scope.load(path);
        } else {
            $scope.navigate(root);
        }
    });
});


'use strict';

angular.module('ajenti.filemanager').controller('FileManagerPropertiesController', function ($scope, $routeParams, $location, notify, filesystem, pageTitle, urlPrefix, gettext) {
    pageTitle.set('path', $scope);

    var modeBits = ['ax', 'aw', 'ar', 'gx', 'gw', 'gr', 'ux', 'uw', 'ur', 'sticky', 'setuid', 'setgid'];
    $scope.permissionsDialogVisible = false;

    $scope.path = $routeParams.path;
    $scope.parent = $scope.path.substring(0, $scope.path.lastIndexOf("/"));
    $scope.refresh = function () {
        return filesystem.stat($scope.path).then(function (info) {
            $scope.info = info;
            $scope.mode = {};
            for (var i = 0; i < modeBits.length; i++) {
                $scope.mode[modeBits[i]] = !!($scope.info.mode & Math.pow(2, i));
            }
        }, function (err) {
            notify.error(gettext('Could not read file information'), err);
        });
    };

    $scope.hidePermissionsDialog = function () {
        return $scope.permissionsDialogVisible = false;
    };

    $scope.applyPermissions = function () {
        $scope.hidePermissionsDialog();

        var mode = 0;
        for (var i = 0; i < modeBits.length; i++) {
            mode += $scope.mode[modeBits[i]] ? Math.pow(2, i) : 0;
        }

        return filesystem.chmod($scope.path, mode).then(function () {
            notify.info(gettext('File mode saved'));
            $scope.refresh();
        });
    };

    $scope.refresh();
});


