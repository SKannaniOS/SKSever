/***
 * This transformation blocks events from reaching a downstream destination if a specifc
 * property contains certain values, e.g., block all Product Added and Order Completed events.
***/

/***
 * JavaScriptCore (which iOS uses under the hood) does not support ES6 module syntax like export or import. 
 * It’s limited to classic (non-module) JavaScript.
 */

function transformEvent(event, metadata) {
    const property = event.event; // Edit property
    const eventlist = ["Product Added", "Order Completed"]; // Edit denylist contents
    const eventPattern = "Single"; // Block any event starting with "Single"

    // Block if exact match in eventlist OR starts with "Single"
    if (property && (eventlist.includes(property) || property.startsWith(eventPattern))) {
        event.event = "SK~" + property; // Prefix the event with "SK~" to indicate it's a custom event
    }
    return event;
}

// Make sure the function is globally available
this.transformEvent = transformEvent;