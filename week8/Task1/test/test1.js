function sleep(time){
    return new Promise((resolve) => setTimeout(resolve, time));
   }
    
async function run(){
console.time('test1_runTime:');
console.log('1');
await sleep(5000);
console.log('2');
// await sleep(1000);
// console.log('3'); 
console.timeEnd('test1_runTime:');
}

run();
console.log('test1');