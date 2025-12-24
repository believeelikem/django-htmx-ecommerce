const form = document.getElementById('user-form')
const submitButton = document.getElementById('submit-btn')

function hasEmailError() {
  const errorEl = form.querySelector('.user-validation-errors')
  return errorEl && errorEl.textContent.trim().length > 1
}

function updateSubmitState() {
  submitButton.disabled = !form.checkValidity() || hasEmailError()
}

if(form){
  form.addEventListener('input', updateSubmitState)
}

document.body.addEventListener('htmx:afterSwap', (e) => {
  if (e.target.classList.contains("user-validation-errors")) {
    updateSubmitState()
  }
})

window.addEventListener('load', updateSubmitState)
