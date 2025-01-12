async function estimateCaloriesByName() {
    const foodName = document.getElementById('food-name').value;
    const result = document.getElementById('calorie-result');
    
    if (foodName.trim() === "") {
        alert("Please enter a food name.");
        return;
    }

    const response = await fetch(`/estimate-calories?food_name=${foodName}`);
    const data = await response.json();

    result.textContent = `${data.calories} kcal`;
}

async function estimateCaloriesByImage() {
    const fileInput = document.getElementById('food-image');
    const result = document.getElementById('calorie-result');

    if (fileInput.files.length === 0) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    const response = await fetch('/estimate-calories-from-image', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    result.textContent = `${data.calories} kcal`;
}
