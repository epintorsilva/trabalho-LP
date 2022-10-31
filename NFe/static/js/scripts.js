document.addEventListener('DOMContentLoaded', () => {
    // Funções para exibir nome do arquivo carregado no botão de upload de arquivo
    let fileInputs = document.querySelectorAll('.file.has-name')
   
    for (let fileInput of fileInputs) {
      let input = fileInput.querySelector('.file-input')
      let name = fileInput.querySelector('.file-name')

      if (input.files.length === 0) {
        name.innerText = 'Nenhum arquivo selecionado'
      } else {
        name.innerText = input.files[0].name
      }

      input.addEventListener('change', () => {
        let files = input.files
        if (files.length === 0) {
          name.innerText = 'Nenhum arquivo selecionado'
        } else {
          name.innerText = files[0].name
        }
      })
    }

    // Funções de ativação/desativação de modal
  function openModal($el) {
    $el.classList.add('is-active');
  }

  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);
    console.log($target)
    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (document.querySelectorAll('.modal-close, .cancel') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener('keydown', (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) { // Escape key
      closeAllModals();
    }
  });
})