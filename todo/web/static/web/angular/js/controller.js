var App = angular.module('App', ['ngResource']);

var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

formatTask = function(task) {

	task.displayName = task.name;

	if (task.completed == true) {
		task.completedClass = "done";
	} else {
		task.completedClass = "not-done";
	}

	if (task.priority == 1) {
		task.priorityClass = "black";
	} else if (task.priority == 2) {
		task.priorityClass = "red";
	} else {
		task.priorityClass = "white";
	}

	if (task.due_date && task.due_date != "clear") {
		// Reconstruct date from yyyy-MM-dd to MM.dd.yyyy
		var parts = task.due_date.split('-');
		task.displayDueDate = parts[1] + "." + parts[2] + "." + parts[0];
		task.dueDateVisibleClass = "show";
		task.calendarVisibleClass = "hide";
	} else {
		task.due_date = "";
		task.displayDueDate = "";
		task.dueDateVisibleClass = "hide";
		task.calendarVisibleClass = "show";
	}

	return task;
};

function Ctrl($scope) {
	$scope.template = "/static/web/angular/templates/task.html";
}

App.controller('TaskListCtrl', function($scope, $http) {

	// Sort by
	$scope.loadTasksOrderByDueDate = function() {
		$http.get('api/tasks').success(function(data) {
			$scope.tasks = data.tasks;
			$scope.tasks.forEach(function(task) {
				formatTask(task);
			});
		});

		$scope.orderByPriorityClass = "text-muted";
		$scope.orderByDueDateClass = "text-primary";
	};

	$scope.loadTasksOrderByPriority = function() {
		$http.get('api/tasks?sorted_by=priority').success(function(data) {
			$scope.tasks = data.tasks;
			$scope.tasks.forEach(function(task) {
				formatTask(task);
			});
		});

		$scope.orderByPriorityClass = "text-primary";
		$scope.orderByDueDateClass = "text-muted";
	};

	// Load tasks
	$scope.loadTasksOrderByDueDate();

	// Add task.
	$scope.newTask = function(taskName) {
		if (!taskName || taskName == "")
			return false;

		$http.post('/api/task/add', {
			"name" : taskName
		}, {
			"headers" : {
				"X-CSRFToken" : csrfmiddlewaretoken
			}
		}).success(function(data) {
			var newTask = data.task;
			newTask = formatTask(newTask);
			$scope.tasks.unshift(newTask);
			$scope.taskName = '';
		});
	};

	$scope.newTaskEnter = function(event, taskName) {

		if (event.which != 13)
			return false;

		$scope.newTask(taskName);
	};

	// Delete task
	$scope.deleteTask = function(task) {
		$http.post('/api/task/delete', {
			"id" : task.id
		}, {
			"headers" : {
				"X-CSRFToken" : csrfmiddlewaretoken
			}
		}).success(function(data) {
			// Remove task from array;
			var i = $scope.tasks.indexOf(task);

			if (i != -1) {
				$scope.tasks.splice(i, 1);
			}
		});
	};

	// Edit task
	$scope.editTask = function(oldTask, task) {

		var data = {
			"id" : task.id,
			"name" : task.name,
			"completed" : task.completed,
			"priority" : task.priority
		};
		
		if (task.due_date != "") {
			data.due_date = task.due_date;
		}

		$http.post('/api/task/edit', $.param(data), {
			"headers" : {
				"X-CSRFToken" : csrfmiddlewaretoken,
				'Content-Type' : 'application/x-www-form-urlencoded'
			}
		}).success(function(data) {
			// Swap task in array;
			var i = $scope.tasks.indexOf(oldTask);

			if (i != -1) {
				$scope.tasks[i] = angular.copy(formatTask(task));
			}
		});
	};

	// Toggle priority
	$scope.togglePriority = function(task) {

		var newTask = angular.copy(task);

		if (task.priority == 0) {
			newTask.priority = 1;
		} else if (task.priority == 1) {
			newTask.priority = 2;
		} else {
			newTask.priority = 0;
		}

		$scope.editTask(task, newTask);
	};

	// Toggle completed
	$scope.toggleCompleted = function(task) {

		var newTask = angular.copy(task);

		if (task.completed) {
			newTask.completed = false;
		} else {
			newTask.completed = true;
		}

		$scope.editTask(task, newTask);
	};

	// Edit task name
	$scope.editTaskName = function(task) {
		if (task.displayName != "" && task.displayName != task.name) {
			var newTask = angular.copy(task);
			newTask.name = task.displayName;
			$scope.editTask(task, newTask);
		} else {
			task.displayName = task.name;
		}
	};

	$scope.editTaskNameKeyPress = function(event, task) {

		if (event.which != 13)
			return false;

		$scope.editTaskName(task);
	};

	// Edit due date
	$scope.editDueDate = function(task) {

		// Reconstruct date from MM.dd.yyyy to yyyy-MM-dd
		var newDate = "clear";
		if (task.displayDueDate != "") {
			var parts = task.displayDueDate.split('.');
			newDate = parts[2] + '-' + parts[0] + '-' + parts[1];
		}

		if (newDate != task.due_date) {
			var newTask = angular.copy(task);
			newTask.due_date = newDate;
			$scope.editTask(task, newTask);
		}
	};
});

App.directive('datepicker', function() {
	return {
		restrict : 'A',
		require : 'ngModel',
		link : function(scope, element, attrs, ngModelCtrl) {
			$(function() {
				element.datepicker({
					format : "mm.dd.yyyy",
					autoclose : true,
					clearBtn : true,
					todayHighlight : true,
					orientation: "right top"
				});
			});
		}
	};
});
