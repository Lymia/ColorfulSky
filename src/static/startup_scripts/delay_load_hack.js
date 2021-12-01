// priority: 100000

console.log("Sleeping for 5 seconds to allow JAOPCA to run. Hopefully.")

let start = Date.now()
while(true) {
    let end = Date.now()
    let elapsed = end - start // elapsed time in milliseconds
    if (elapsed > 5000) break;
}
