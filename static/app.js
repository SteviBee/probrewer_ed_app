console.log("hello world ")


// TODO - make JS for course to change highlighting of module name if name changes for sub mod on question
// EXTRA TODO from ^^^ - add cool animation when transition from one mod to another 

$("#nav-course").on("click", function() {
    window.scroll(0, 1000)
});

// async function getData(){
//     // let response = await axios.post("/api/get-lucky-num", {"name":"1", "email": "fizz@bizz", "year": "1990", "color": "blue"})
//     // let response = await axios.post("/api/get-lucky-num", json, {
//     //     headers: {
//     //       'Content-Type': 'application/json'
//     //     },
//     // });
//     let response = await axios.post("/api/get-lucky-num", form_data)
//     console.log("getCard resp=", response.data);

//     handleResponse(response.data)
//     // if (response.data.ans){
//     //     handleResponse(response.data.ans)
//     // } else {
//     //     handleResponse(response.data.error)
//     // }
// }
// getData();

// function handleResponse(resp) {

//     if (resp.error) {
//         for (const key in resp.error) {
      
//             $(`#${key}-err`).append(`<p>${resp.error[key]}</p>`)
                
//         }   

//     } else {
      
//         $(`#lucky-results`).append(`<p>Your lucky number is ${resp.ans.num.num} ${resp.ans.num.fact}</p>`)
//         $(`#lucky-results`).append(`<p>Your birth year ${resp.ans.year.year} fact is ${resp.ans.year.fact}</p>`)


//     }


// }