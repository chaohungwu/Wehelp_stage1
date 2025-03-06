function sleep(time){
    return new Promise((resolve) => setTimeout(resolve, time));
   }
    
async function run(){
console.time('test2_runTime:');
console.log('1');
await sleep(3000);
// console.log('2');
// await sleep(1000);
// console.log('3'); 
console.timeEnd('test2_runTime:');
}

run();
console.log('test2');