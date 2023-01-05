import { API_URL } from ".";

export async function fetchWishlist(slug: string, page = 1) {
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
