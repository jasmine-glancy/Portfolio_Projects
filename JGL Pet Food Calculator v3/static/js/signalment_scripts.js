window.addEventListener('DOMContentLoaded', () => {
    const selectedSex = document.getElementById('sex');
    selectedSex.addEventListener('change', selectFemale);

    const pregnancySelect = document.getElementById('gestating');
    pregnancySelect.addEventListener('change', selectFemale);

    const speciesSelect = document.getElementById('species');
    speciesSelect.addEventListener('change', selectFemale)

    const lacationSelect = document.getElementById('weeks_lactating');
    lacationSelect.addEventListener('change', selectLacation)

    function selectFemale() {
        var sex = selectedSex.value;
        var gestating = pregnancySelect.value;
        var species = speciesSelect.value;
        if (sex == 'female' && species == 'canine') {
            // If pet is an intact female, show nursing/pregnant questions
            document.getElementById("repro_questions").style.display = 'block';
            if (gestating == 'y') {
                // If pet is pregnant and canine, ask how many weeks along she is
                document.getElementById("gestation").style.display = 'block';
                document.getElementById("nursing_questions").style.display = 'none';
    
            }
            else if (gestating == 'n') {
                // If pet is not pregnant, ask if she is currently nursing a litter
                document.getElementById("nursing_questions").style.display = 'block';
            }
            else {
                // Otherwise, hide nursing questions
                document.getElementById("gestation").style.display = 'none';
                document.getElementById("nursing_questions").style.display = 'none';
            }
        }
        else if (sex == 'female' && species == 'feline') {
            // If pet is an intact female, show nursing/pregnant questions
            document.getElementById("repro_questions").style.display = 'block';
            if (gestating == 'n') {
                // If pet is not pregnant, ask if she is currently nursing a litter
                document.getElementById("nursing_questions").style.display = 'block';
            }
            else {
                // Otherwise, hide nursing questions
                document.getElementById("nursing_questions").style.display = 'none';
            }
        }
        else {
            // Otherwise, hide them
            document.getElementById("repro_questions").style.display = 'none';
            document.getElementById("gestation").style.display = 'none';
            document.getElementById("nursing_questions").style.display = 'none';
        }
    }
    
    function selectLacation() {
        var species = speciesSelect.value;
        var lactating = lacationSelect.value;
        
        if (lactating == 'y' && species == 'feline') {
            // If nursing and feline, ask how many weeks she has been lactating
            document.getElementById("weeks_lactating").style.display = 'block';
        }
        else {
            document.getElementById("weeks_lactating").style.display = 'none';
        }
    }
    // Call functions once on page load to set initial visibility
    selectFemale();
    selectLacation();
})