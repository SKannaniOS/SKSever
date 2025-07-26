/***
 * This transformation blocks events from reaching a downstream destination if a specifc
 * property contains certain values, e.g., block all Product Added and Order Completed events.
***/

export function transformEvent(event, metadata) {
    const property = event.event; // Edit property
    const denylist = ["Product Added", "Order Completed"]; // Edit denylist contents
    const denyPattern = "Home"; // Block any event starting with "Home"
    
    // Block if exact match in denylist OR starts with "Home"
    if (property && (denylist.includes(property) || property.startsWith(denyPattern))) return;
    return event;
}