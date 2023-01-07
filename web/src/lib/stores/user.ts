import { writable } from 'svelte/store';

function createUserStore() {
  const {subscribe, set, update} = writable(null);

  function userSubscribe() {


  }

  return {
    subscribe: userSubscribe,
  }


}


export const user = createUserStore();
