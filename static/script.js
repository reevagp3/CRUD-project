// Use relative path so it works both locally and on Render in production
const API = "/api";

// 🌗 TOGGLE THEME
function toggleTheme() {
    document.body.classList.toggle("light");
}

// 🔔 TOAST MESSAGE
function showToast(msg) {
    let toast = document.getElementById("toast");
    toast.innerText = msg;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2000);
}

// 📦 LOAD ITEMS
async function loadItems() {
    try {
        let res = await fetch(API + "/items");
        let data = await res.json();

        let container = document.getElementById("items");
        container.innerHTML = "";

        if (!data || data.length === 0) {
            container.innerHTML = `
                <div class="empty-message">
                    No items found
                </div>
            `;
            return;
        }

        data.forEach(item => {
            container.innerHTML += `
                <div class="item">
                    <span>📌 ${item.name}</span>

                    <div class="btns">
                        <button 
                            class="edit-btn" 
                            onclick="editItem(${item.id})"
                        >
                            ✏️
                        </button>

                        <button 
                            class="delete-btn" 
                            onclick="deleteItem(${item.id})"
                        >
                            🗑
                        </button>
                    </div>
                </div>
            `;
        });

    } catch (error) {
        console.error(error);
        showToast("Failed to load items");
    }
}

// ➕ ADD ITEM
async function addItem() {
    let name = document.getElementById("name").value.trim();

    if (!name) {
        showToast("Please enter something");
        return;
    }

    try {
        let res = await fetch(API + "/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name })
        });

        let result = await res.json();

        if (res.ok) {
            document.getElementById("name").value = "";
            loadItems();
            showToast("Item added successfully");
        } else {
            showToast(result.error || "Add failed");
        }

    } catch (error) {
        console.error(error);
        showToast("Server error");
    }
}

// ✏️ EDIT ITEM
async function editItem(id) {
    let newName = prompt("Update value:");

    if (!newName || !newName.trim()) return;

    try {
        let res = await fetch(API + "/update/" + id, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: newName.trim()
            })
        });

        let result = await res.json();

        if (res.ok) {
            loadItems();
            showToast("Updated successfully");
        } else {
            showToast(result.error || "Update failed");
        }

    } catch (error) {
        console.error(error);
        showToast("Server error");
    }
}

// 🗑 DELETE ITEM
async function deleteItem(id) {
    try {
        let res = await fetch(API + "/delete/" + id, {
            method: "DELETE"
        });

        let result = await res.json();

        if (res.ok) {
            loadItems();
            showToast("Deleted successfully");
        } else {
            showToast(result.error || "Delete failed");
        }

    } catch (error) {
        console.error(error);
        showToast("Server error");
    }
}

// 🚀 INITIAL LOAD
loadItems();