const filter = document.getElementById('filter');
const customers = document.getElementsByClassName('searchable');

filter.addEventListener('input', (e) => filterData(e.target.value));

function filterData(searchTerm) {
  Array.from(customers).forEach((customer) => {
    const paragraphElement = customer.getElementsByTagName('p')[0].innerHTML
    if (paragraphElement.toLowerCase().includes(searchTerm.toLowerCase())) {
      customer.classList.remove('d-none');
    } else {
      customer.classList.add('d-none');
    };
  });
};