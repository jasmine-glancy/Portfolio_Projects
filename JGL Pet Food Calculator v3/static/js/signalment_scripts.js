window.addEventListener('DOMContentLoaded', () => {
    const selectedSex = document.getElementById('sex');
    selectedSex.addEventListener('change', selectFemale);

    const pregnancySelect = document.getElementById('gestating');
    pregnancySelect.addEventListener('change', selectGestation);

    const speciesSelect = document.getElementById('species');
    speciesSelect.addEventListener('change', selectFemale)

    const lacationSelect = document.getElementById('weeks_lactating');
    lacationSelect.addEventListener('change', selectLacation)


    function selectFemale() {
        var sex = selectedSex.value;
        if (sex == 'female') {
            // If pet is an intact female, show nursing/pregnant questions
            document.getElementById("repro_questions").style.display = 'block';
            selectGestation(); // Call selectGestation to decide to show nursing_questions or not, suggested by CoPilot
        }
        else {
            // Otherwise, hide them
            document.getElementById("repro_questions").style.display = 'none';
            document.getElementById("nursing_questions").style.display = 'none';

        }
    }
    
    function selectGestation() {
        var gestating = pregnancySelect.value;
        var species = speciesSelect.value;
        var sex = selectedSex.value;

        if (sex == 'female' && gestating == 'y' && species == 'canine') {
            // If pet is pregnant and canine, ask how many weeks along she is
            document.getElementById("gestation").style.display = 'block';
            document.getElementById("nursing_questions").style.display = 'none';

        }
        else if (sex == 'female' && gestating == 'n') {
            // If pet is not pregnant, ask if she is currently nursing a litter
            document.getElementById("nursing_questions").style.display = 'block';
        }
        else {
            // If gestating is neither 'y' nor 'n', hide both divs
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
    selectGestation();
    selectLacation();
})