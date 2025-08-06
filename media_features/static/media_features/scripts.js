document.addEventListener('DOMContentLoaded', function() {
    const departmentSelect = document.getElementById('id_department');
    const offeringsContainer = document.getElementById('curricular-offerings-container');
    const m2mField = document.getElementById('id_curricular_offerings');

    // Function to fetch and display offerings
    function updateCurricularOfferings() {
        const departmentId = departmentSelect.value;
        offeringsContainer.innerHTML = ''; // Clear existing checkboxes

        if (!departmentId) {
            return; // Do nothing if no department is selected
        }

        // Construct the URL using the department ID
        const url = `/get-curricular-offerings/${departmentId}/`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.length > 0) {
                    data.forEach(offering => {
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.id = `id_curricular_offerings_${offering.curricular_offering_id}`;
                        checkbox.name = 'curricular_offerings';
                        checkbox.value = offering.curricular_offering_id;

                        const label = document.createElement('label');
                        label.htmlFor = checkbox.id;
                        label.textContent = offering.offering_name;

                        const div = document.createElement('div');
                        div.className = 'curricular-item';
                        div.appendChild(checkbox);
                        div.appendChild(label);

                        offeringsContainer.appendChild(div);
                    });
                } else {
                    offeringsContainer.innerHTML = '<p>No curricular offerings for this department.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching curricular offerings:', error);
                offeringsContainer.innerHTML = '<p>Error loading offerings.</p>';
            });
    }

    // Event listener for department selection change
    departmentSelect.addEventListener('change', updateCurricularOfferings);

    // Initial call to populate the field if a department is already selected on page load
    // This is useful for forms that have pre-filled data
    if (departmentSelect.value) {
        updateCurricularOfferings();
    }
});