$(document).ready(() => {

    let createMode = false;

    $.get("/tasks", (data) => {
        tasks = data.tasks;
        
        if (tasks.length === 0) {
            $("#taskList").append("You have no tasks that need completed!");
        }

        for (const task of tasks) {
            $("#taskList").append(`<li class="nav-item" rel="popover" data-placement="right" data-content="${task.description}" 
                data-trigger="hover"><a class="nav-link active" href="${task.uri}" id="${task.id}" data-toggle="modal" 
                data-target="#exampleModal" data-done="${task.done}">${task.title}</a></li><br>`)

            $(`#${task.id}`).parent().popover();
        }
    });

    $("#taskList").on("click", "li a", (e) => {
        e.preventDefault();
    })

    $("#exampleModal").on("show.bs.modal", function(e) {
        const button = $(e.relatedTarget);
        const modal = $(this);
        let submit = modal.find("#submit");
        let title = button.text();
        let url = button.attr("href");

        createMode = button.data("create");

        if (createMode) {
            modal.find("#done").parent().hide();
            modal.find(".modal-title").text(title);

            submit.on("click", (e) => {
                e.preventDefault();

                if (!modal.find("#title").val() || !modal.find("#description").val()) {
                    // psuedo validation??
                    return;
                }

                const obj = {
                    title: modal.find("#title").val(),
                    description: modal.find("#description").val()
                }

                $.ajax({
                    contentType: "application/json",
                    url: "/tasks",
                    type: "POST",
                    data: JSON.stringify(obj),
                    success: (data) => {
                        location.reload();
                        console.log(data);
                    }
                });
            });
        }
        if (!createMode) {
            modal.find("#done").parent().show();
            const id = e.relatedTarget.id;
            const description = button.parent().data("content");
            const done = button.data("done");

            modal.find(".modal-title").text("Editing task : " + title);
            modal.find("#title").val(title);
            modal.find("#description").val(description);
            modal.find("#done").prop("checked", done);

            submit.on("click", (e) => {
                e.preventDefault();

                const obj = {
                    id: id,
                    title: modal.find("#title").val(),
                    description: modal.find("#description").val(),
                    done: modal.find("#done").is(":checked")
                }

                $.ajax({
                    contentType: "application/json",
                    url: url,
                    type: "PUT",
                    data: JSON.stringify(obj),
                    success: (data) => {
                        location.reload();
                        console.log(data);
                    }
                });
            });
        }
    });

    $("#exampleModal").on("hide.bs.modal", function(e) {
        const modal = $(this);
        modal.find("#title").val("");
        modal.find("#description").val("");
        createMode = false;
    });
});