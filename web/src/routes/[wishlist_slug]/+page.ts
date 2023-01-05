import {fetchWishlist} from '$lib/api/wishlist'

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
  console.log("hello");
  const items = await fetchWishlist(params.wishlist_slug)
  console.log(items)
  return items
  
  
  return {
    wishlist: {
      name: `Wishlist name`,
      slug: params.wishlist_slug,
      description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      image_url: 'https://picsum.photos/id/99/400/800',
      items: [
        {
          name: 'Fiskars knife',
          description: 'I want the 37cm or the 36 cm one.',
          image_url: `https://picsum.photos/id/101/300?blur`,
          quantity: 2,
          reserved: 0,
          price: 14.88,
          url: 'https://example.com',
          message_count: 0,
        },
        {
          name: 'Craft beer',
          description: 'Anything is fine :)',
          image_url: 'https://picsum.photos/id/102/200?blur',
          quantity: 0,
          reserved: 3,
          price: null,
          url: 'https://example.com',
          message_count: 2,
        },
        {
          name: 'Stun baton',
          description: 'Telescopic',
          image_url: 'https://picsum.photos/id/103/200?blur',
          quantity: 1,
          reserved: 1,
          price: 80,
          message_count: 10,
        },
        {
          name: 'Candy',
          image_url: 'https://picsum.photos/id/104/200?blur',
          quantity: 12,
          reserved: 1,
          price: 8,
          url: 'https://example.com',
          message_count: 0,
        },
      ]
    }
  };
}

