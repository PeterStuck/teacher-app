function paste_ms_teams_formula(isMale) {
    let topic = document.querySelector('#id_comments');
        if (isMale) {
            topic.value = 'MS Teams. Zajęcia dostosowane do możliwości i potrzeb ucznia.';
        }
        else {
            topic.value = 'MS Teams. Zajęcia dostosowane do możliwości i potrzeb uczennicy.';
        }
    }

    function paste_stacionary_class_formula() {
        let topic = document.querySelector('#id_comments');
        topic.value = 'Zajęcia stacjonarne.';
    }