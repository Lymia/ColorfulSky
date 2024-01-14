// priority: 100000
// side: startup

console.log("Sleeping for 3 seconds to allow JAOPCA to run. Hopefully.")

let start = Date.now()
while(true) {
    let end = Date.now()
    let elapsed = end - start // elapsed time in milliseconds
    if (elapsed > 3000) break;
}
