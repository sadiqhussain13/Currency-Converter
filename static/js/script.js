// Fetch conversion rates and update result
document.getElementById("convert-btn").addEventListener("click", async () => {
    const amount = document.getElementById("amount").value;
    const base = document.getElementById("base-currency").value;
    const target = document.getElementById("target-currency").value;

    try {
        const response = await fetch(`/api/convert?base=${base}&target=${target}&amount=${amount}`);
        const data = await response.json();

        if (data.status === "success") {
            document.getElementById("conversion-result").innerText =
                `${amount} ${base} equals ${data.converted_amount} ${target}`;
            loadGraph(base, target);
        } else {
            alert("Error fetching conversion rates!");
        }
    } catch (error) {
        console.error("Error:", error);
    }
});

// Fetch historical data and render graph
async function loadGraph(base, target) {
    try {
        const response = await fetch(`/api/historical?base=${base}&target=${target}`);
        const data = await response.json();

        const labels = Object.keys(data);
        const rates = Object.values(data);

        const ctx = document.getElementById("exchange-rate-graph").getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: `${base} to ${target}`,
                        data: rates,
                        borderColor: "#4285f4",
                        fill: false,
                        tension: 0.1,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: "Date" } },
                    y: { title: { display: true, text: "Exchange Rate" } },
                },
            },
        });
    } catch (error) {
        console.error("Error fetching historical data:", error);
    }
}

// Initial graph load on page load
loadGraph("EUR", "INR");