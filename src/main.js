import './style.css'
import { setupCounter } from './counter.js'

document.querySelector('#app').innerHTML = `
<section id="center">
  <div>
    <h1>Audito</h1>
    <p>Best music reviewing platform</p>
  </div>
  <button id="counter" type="button" class="counter"></button>
</section>
`

setupCounter(document.querySelector('#counter'))
