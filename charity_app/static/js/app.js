document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // // Form submit
      // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  const nextStepButtons = document.querySelectorAll(".next-step");
  const checkboxes = document.querySelectorAll("input[name='categories']");
  const institutions = document.querySelectorAll('.form-group.organisation')

  console.log("Next step buttons:", nextStepButtons);
  console.log("Checkboxes:", checkboxes);

  nextStepButtons.forEach(button => {
    button.addEventListener('click', function () {
      // check if correct step
      const currentStep = button.closest('[data-step]')



      // if (currentStep.getAttribute('data-step') !== '1'){
      //   return
      // }

      // Get selected categories
      let selectedCategories = [];
      checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
          selectedCategories.push(checkbox.value)
        }
      });


      // Filter institutions
      institutions.forEach(institution =>{
        // console.log('Instytucja:', institution)
        // console.log('Kategorie instytucji:', institution.getAttribute('data-categories'))
        const institutionCategories = institution.getAttribute('data-categories').split(',');
        let match = selectedCategories.every(category =>
          institutionCategories.includes(category)
        )
        if (match) {
          institution.style.display = 'block';
        }
        else {
          institution.style.display = 'none'
        }
      })



      if (currentStep.getAttribute('data-step') === '4'){
        // number of bags and what categories
        const numberOfBags = document.querySelector('input[name="bags"]').value
        const summaryText = document.getElementById('summary-text')
        summaryText.textContent = `${numberOfBags} ${correctWordForm(numberOfBags)} z kategorii  ${selectedCategories}`

        const chosen_institution = document.querySelector('input[name="institution"]:checked')
        const institutionName = chosen_institution.parentNode.querySelector('.title').textContent
        const summaryInstitution = document.getElementById('summary-institution')
        summaryInstitution.textContent = `Dla organizacji "${institutionName}"`
        function correctWordForm(number_of_bags) {
          number_of_bags = Math.abs(numberOfBags)
          if (number_of_bags === 1) {
            return " worek";
          } else if (number_of_bags < 5) {
            return " worki";
          } else {
            return " worków";
            }
        }
        const addressInput = document.querySelector('input[name="address"]').value
        const address = document.querySelector('.form-section--column ul li')
        address.textContent = `${addressInput}`

        const cityInput = document.querySelector('input[name="city"]').value
        const city = document.querySelectorAll('.form-section--column ul li')[1]
        city.textContent = `${cityInput}`

        const postalCodeInput = document.querySelector('input[name="postcode"]').value
        const postalCode = document.querySelectorAll('.form-section--column ul li')[2]
        postalCode.textContent = `${postalCodeInput}`

        const phoneNumberInput = document.querySelector('input[name="phone"]').value
        const phoneNumber = document.querySelectorAll('.form-section--column ul li')[3]
        phoneNumber.textContent = `${phoneNumberInput}`

        const pickupDateInput = document.querySelector('input[name="date"]').value
        const pickupDate = document.querySelectorAll('.form-section--column.date ul li')[0]
        pickupDate.textContent = `${pickupDateInput}`

        const pickupTimeInput = document.querySelector('input[name="time"]').value
        const pickupTime = document.querySelectorAll('.form-section--column.date ul li')[1]
        pickupTime.textContent = `${pickupTimeInput}`

        const more_infoInput = document.querySelector('textarea[name="more_info"]').value
        console.log('moreinfo', more_infoInput)
        const moreInfo = document.querySelectorAll('.form-section--column.date ul li')[2]
        moreInfo.textContent = `${more_infoInput}`

      }

    })
  })

  const buttons = document.querySelectorAll('button[data-donation-id]')

  buttons.forEach(button => {
  button.addEventListener('click', function () {
    console.log('Button clicked')
    const donationId = this.dataset.donationId;
    const donationItem = button.closest('.donation-item');
    const buttonLabel = button.textContent.trim();
    let is_taken;

    if (buttonLabel === "Oznacz jako 'odebrane'") {
      is_taken = true;
    } else {
      is_taken = false;
    }

    if (donationItem) {
      donationItem.style.color = 'lightgrey'
      donationItem.parentNode.appendChild(donationItem)
    }

    fetch(`/update_donation_status/`, {
      method: 'POST',
      body: JSON.stringify({
        'donation_id': donationId,
        'is_taken': is_taken
      }),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
    }).then(response => {
        if(response.ok) {
            location.reload();
        } else {
            // Handle error here
            console.log('Error updating donation status');
        }
    });
  });
});

});


