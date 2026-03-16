async function awaitable_custom_fetch(url) {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            console.error("HTTP error:", response.status, response.statusText);
            console.error("URL:", url);
            return null;
        }

        return await response.text();
    }
    catch (err) {
        console.error("Network or fetch error");
        console.error("URL:", url);
        console.error(err);
        return null;
    }
}

export default awaitable_custom_fetch;