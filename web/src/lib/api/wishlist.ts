import { API_URL } from ".";

export interface ItemData {
  name: string;
  image_url: string;
  description: string;
  quantity: number;
  reserved: number;
  price: number;
  shop_url: string;
};

export interface WishlistData {
  name: string;
  image_url: string;
  description: string;
};

export interface WishlistIndex extends WishlistData {
  items: [ItemData];
};


export async function fetchWishlist(slug: string, page = 1): Promise<WishlistIndex> {
  console.log('fetch@', `${API_URL}/lists/${slug}?page=${page}`)
  return fetch(`${API_URL}/lists/${slug}?page=${page}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    }
  ).then((response) => response.json());
}


