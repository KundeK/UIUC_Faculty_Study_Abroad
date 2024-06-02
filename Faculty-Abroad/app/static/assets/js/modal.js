$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const firstName = button.data('first_name') // Extract first_name from data-* attributes
        const lastName = button.data('last_name') // Extract last_name from data-* attributes
        const course = button.data('course') // Extract last_name from data-* attributes
        const semester = button.data('semester') // Extract last_name from data-* attributes
        const year = button.data('year') // Extract last_name from data-* attributes
        // const university = button.data('university') // Extract last_name from data-* attributes

        console.log(firstName, lastName, course, semester, year)

        const modal = $(this)
        if (taskID === 'New Experience') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('expId')
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display').attr('expId', taskID)
        }

        // if (firstName) {
        modal.find('.form-first_name').val(firstName);
        modal.find('.form-last_name').val(lastName);
        modal.find('.form-course').val(course);
        modal.find('.form-semester').val(semester);
        modal.find('.form-year').val(year);
        // modal.find('.form-university').val(university);
        // } else {
        //     modal.find('.form-first_name').val('');
        //     modal.find('.form-last_name').val('');
        // }
    })


    $('#submit-task').click(function () {
        const tID = $('#task-form-display').attr('expId');
        console.log($('#task-modal').find('.form-first_name').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'first_name': $('#task-modal').find('.form-first_name').val(),
                'last_name': $('#task-modal').find('.form-last_name').val(),
                'course': $('#task-modal').find('.form-course').val(),
                'semester': $('#task-modal').find('.form-semester').val(),
                'year': $('#task-modal').find('.form-year').val(),
                // 'university': $('#task-modal').find('.form-university').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
                console.log('Page reloaded');
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.state').click(function () {
        const state = $(this)
        const tID = state.data('source')
        let new_state
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});