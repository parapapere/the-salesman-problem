<script setup>

import { ref } from 'vue';
import axios from "axios";

const httpOrsApi = axios.create({
  headers: {
    common: { Accept: 'application/json, text/plain' }
  }
});

const optimalPath = ref();
const optimalDistance = ref(null);
const locations = ref([]);
const inputValue1 = ref();
const inputValue2 = ref();
const distanceMatrix = ref([]);

const addPoint = async () => {

  locations.value.push([inputValue1.value, inputValue2.value])
  console.log(locations.value);
  try {
    const url = 'https://api.openrouteservice.org/v2/matrix/driving-car';
    const apiKey = '5b3ce3597851110001cf6248ddae57dc913a48c1895c9c2e3724067d';
    const body = {
      locations: locations.value
    };

    // Pobierz macierz odległości z API OpenRouteService
    const response = await httpOrsApi.post(`${url}?api_key=${apiKey}`, body);
    distanceMatrix.value = response.data.durations;
    console.log(locations.value);
    console.log(distanceMatrix.value);
  } catch (error) {
    console.error(error.response);
  }
};

// const addPoint = async () => {
//   locations.value.push([inputValue1.value, inputValue2.value]);
//   console.log(locations.value.map(([lon, lat]) => `${lat},${lon}`),)

//   try {
//     const url = 'https://graphhopper.com/api/1/matrix';
//     const apiKey = '4747e0f7-5609-447c-98cb-1dd44b42363d'; // Twój klucz API GraphHopper
//     const body = {
//       point: locations.value,
//       key: apiKey,
//       vehicle: 'car',
//     };

//     // Pobierz macierz odległości z API GraphHopper
//     const response = await axios.post(url, body);
//     distanceMatrix.value = response.data.distances;
//     console.log(locations.value);
//     console.log(distanceMatrix.value);
//   } catch (error) {
//     console.error(error);
//   }
// };

const getOptimalPath = async () => {

  try {

    // Wywołaj endpoint FastAPI z uzyskaną macierzą odległości
    const fastApiUrl = 'http://localhost:5000/count_optimal/';
    const fastApiResponse = await axios.post(fastApiUrl, distanceMatrix.value);
    const { path, cost } = fastApiResponse.data;

    optimalPath.value = path.join('-');
    optimalDistance.value = cost;
	console.log(optimalPath.value)
  } catch (error) {
    console.error(error);
  }
};

getOptimalPath()

</script>

<template>
	<h1>Problem Komiwojażera - Interfejs</h1>
  
  <label for="coordinate-x">Współrzędna X:</label>
  <input v-model="inputValue1" type="number" >
  
  <label for="coordinate-y">Współrzędna Y:</label>
  <input v-model="inputValue2" type="number" >
  
  <button @click="addPoint()">Dodaj punkt</button>
  
  <h2>Macierz dystansu:</h2>
  <table class="bordered-table">
    <tbody>
      <tr v-for="(row, rowIndex) in distanceMatrix" :key="rowIndex">
        <td v-for="(distance, colIndex) in row" :key="colIndex" class="centered-cell">{{ distance }}</td>
      </tr>
    </tbody>
  </table>

  <button @click="getOptimalPath()">Oblicz najkrutsza sciezke</button>
  
  <h2>Najkrótsza ścieżka:</h2>
  <div>{{ optimalPath }}</div>

  <h2>Dystans:</h2>
  <div id="shortest-path">{{ optimalDistance/1000 }}</div>
</template>

<style>
label {
  display: block;
  margin-bottom: 5px;
}
input[type="text"] {
  width: 200px;
  margin-bottom: 10px;
}
#points-list {
  margin-bottom: 10px;
}
.bordered-table {
  border-collapse: collapse;
}

.bordered-table td {
  border: 1px solid black;
  padding: 8px;
}

.centered-cell {
  text-align: center;
}
</style>


