var App = angular.module('App', ['ngResource'/*, 'ngAnimate'*/]);
var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

formatTask = function(task) {

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

	if (!task.due_date) {
		task.calendarClass = "show";
		task.due_dateRank = "9999-99-99";
	} else {
		task.due_dateRank = task.due_date;
		parts = task.due_date.split('-');
		task.due_dateFormat = parts[2] + "." + parts[1] + "." + parts[0];
		task.calendarClass = "hide";
	}

	return task;
};

function Ctrl($scope) {
	$scope.template = "/static/web/angular/templates/task.html";
}

App.controller('TaskListCtrl', function($scope, $http) {

	// Load tasks
	$http.get('api/tasks').success(function(data) {
		$scope.tasks = data.tasks;
		$scope.tasks.forEach(function(task) {
			formatTask(task);
		});

		$scope.orderProp = ['due_dateRank', '-priority', 'id'];
	});

	// Sort by
	$scope.orderByDueDate = function() {
		$scope.orderProp = ['due_dateRank', '-priority', 'id'];
	};

	$scope.orderByPriority = function() {
		$scope.orderProp = ['-priority', 'due_dateRank', 'id'];
	};

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
			$scope.tasks.push(newTask);
			$scope.taskName = '';
		});
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
				'Content-Type': 'application/x-www-form-urlencoded'
			}
		}).success(function(data) {
			// Swap task in array;
			var i = $scope.tasks.indexOf(oldTask);

			if (i != -1) {
				$scope.tasks.splice(i, 1);
			}
			
			formatTask(task);
			
			$scope.tasks.push(task);
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
});
