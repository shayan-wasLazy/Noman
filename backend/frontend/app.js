// ============================================================
// CONFIG
// ============================================================

const NODE_TIMEOUT = 5;

const UPDATE_INTERVAL = 1000;


// ============================================================
// CHART CREATION
// ============================================================

function createChart(
    canvasId
) {

    return new Chart(
        document.getElementById(
            canvasId
        ),
        {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    {
                        label: "X",
                        data: [],
                        tension: 0.25,
                        borderWidth: 2,
                        pointRadius: 0
                    },

                    {
                        label: "Y",
                        data: [],
                        tension: 0.25,
                        borderWidth: 2,
                        pointRadius: 0
                    },

                    {
                        label: "Z",
                        data: [],
                        tension: 0.25,
                        borderWidth: 2,
                        pointRadius: 0
                    }

                ]

            },


            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: false,

                interaction: {

                    intersect: false,

                    mode: "index"

                },


                scales: {

                    x: {

                        ticks: {

                            color:
                                "#718096",

                            maxTicksLimit:
                                10

                        },

                        grid: {

                            color:
                                "#1c2530"

                        }

                    },


                    y: {

                        ticks: {

                            color:
                                "#718096"

                        },

                        grid: {

                            color:
                                "#1c2530"

                        }

                    }

                },


                plugins: {

                    legend: {

                        labels: {

                            color:
                                "#aeb8c4"

                        }

                    }

                }

            }

        }
    );
}


// ============================================================
// CHARTS
// ============================================================

const charts = {

    NODE_01:
        createChart(
            "node1Chart"
        ),

    NODE_02:
        createChart(
            "node2Chart"
        )

};


// ============================================================
// UPDATE CHART
// ============================================================

function updateChart(
    nodeId,
    history
) {

    const chart =
        charts[nodeId];


    if (!chart) {
        return;
    }


    chart.data.labels =
        history.map(
            item => {

                if (
                    !item.timestamp
                ) {
                    return "";
                }


                return new Date(
                    item.timestamp
                ).toLocaleTimeString();

            }
        );


    chart.data.datasets[0].data =
        history.map(
            item =>
                Number(item.x)
        );


    chart.data.datasets[1].data =
        history.map(
            item =>
                Number(item.y)
        );


    chart.data.datasets[2].data =
        history.map(
            item =>
                Number(item.z)
        );


    chart.update(
        "none"
    );
}


// ============================================================
// ONLINE STATUS
// ============================================================

function isOnline(
    data
) {

    if (
        !data ||
        !data.timestamp
    ) {

        return false;

    }


    const timestamp =
        new Date(
            data.timestamp
        ).getTime();


    const age =
        (
            Date.now() -
            timestamp
        ) / 1000;


    return (
        age <= NODE_TIMEOUT
    );
}


// ============================================================
// NODE CARD
// ============================================================

function nodeCard(
    nodeId,
    data
) {

    const online =
        isOnline(data);


    const x =
        Number(
            data?.x ?? 0
        );

    const y =
        Number(
            data?.y ?? 0
        );

    const z =
        Number(
            data?.z ?? 0
        );


    return `

        <div class="node-card">

            <div class="node-header">

                <div class="node-name">
                    ${nodeId}
                </div>

                <div class="node-state">

                    <span
                        class="node-state-dot ${
                            online
                                ? "online"
                                : "offline"
                        }">
                    </span>

                    ${
                        online
                            ? "ONLINE"
                            : "OFFLINE"
                    }

                </div>

            </div>


            <div class="readings">

                <div class="reading">

                    <div class="reading-label">
                        X AXIS
                    </div>

                    <div class="reading-value">
                        ${x.toFixed(3)}
                    </div>

                    <span class="reading-unit">
                        g
                    </span>

                </div>


                <div class="reading">

                    <div class="reading-label">
                        Y AXIS
                    </div>

                    <div class="reading-value">
                        ${y.toFixed(3)}
                    </div>

                    <span class="reading-unit">
                        g
                    </span>

                </div>


                <div class="reading">

                    <div class="reading-label">
                        Z AXIS
                    </div>

                    <div class="reading-value">
                        ${z.toFixed(3)}
                    </div>

                    <span class="reading-unit">
                        g
                    </span>

                </div>

            </div>

        </div>

    `;
}


// ============================================================
// GET LATEST DATA
// ============================================================

async function fetchLatest()
{

    const response =
        await fetch(
            "/api/sensors"
        );


    if (!response.ok) {

        throw new Error(
            "API unavailable"
        );

    }


    return await response.json();
}


// ============================================================
// GET NODE HISTORY
// ============================================================

async function fetchNodeHistory(
    nodeId
) {

    const response =
        await fetch(
            `/api/sensor/${nodeId}/history`
        );


    if (!response.ok) {
        return [];
    }


    const result =
        await response.json();


    return result.history || [];
}


// ============================================================
// UPDATE DASHBOARD
// ============================================================

async function updateDashboard()
{

    try {

        const sensors =
            await fetchLatest();


        // ----------------------------------------------------
        // Backend
        // ----------------------------------------------------

        document.getElementById(
            "systemDot"
        ).style.background =
            "#22c55e";


        document.getElementById(
            "systemStatus"
        ).textContent =
            "Backend connected";


        // ----------------------------------------------------
        // Force exactly two nodes
        // ----------------------------------------------------

        const nodeIds = [
            "NODE_01",
            "NODE_02"
        ];


        let online =
            0;


        // ----------------------------------------------------
        // Cards
        // ----------------------------------------------------

        const container =
            document.getElementById(
                "nodesContainer"
            );


        container.innerHTML =
            nodeIds.map(
                nodeId => {

                    const data =
                        sensors[nodeId];


                    if (
                        isOnline(data)
                    ) {

                        online++;

                    }


                    return nodeCard(
                        nodeId,
                        data
                    );

                }
            ).join("");


        // ----------------------------------------------------
        // Overview
        // ----------------------------------------------------

        document.getElementById(
            "totalNodes"
        ).textContent =
            "2";


        document.getElementById(
            "onlineNodes"
        ).textContent =
            online;


        document.getElementById(
            "offlineNodes"
        ).textContent =
            2 - online;


        document.getElementById(
            "lastUpdate"
        ).textContent =
            new Date().toLocaleTimeString();


        // ----------------------------------------------------
        // History
        // ----------------------------------------------------

        for (
            const nodeId of nodeIds
        ) {

            const history =
                await fetchNodeHistory(
                    nodeId
                );


            updateChart(
                nodeId,
                history
            );


            const status =
                document.getElementById(
                    nodeId === "NODE_01"
                        ? "node1ChartStatus"
                        : "node2ChartStatus"
                );


            if (status) {

                status.textContent =
                    `${history.length} samples`;

            }

        }

    }

    catch (error) {

        console.error(
            error
        );


        document.getElementById(
            "systemDot"
        ).style.background =
            "#ef4444";


        document.getElementById(
            "systemStatus"
        ).textContent =
            "Backend offline";

    }

}


// ============================================================
// START
// ============================================================

updateDashboard();


setInterval(
    updateDashboard,
    UPDATE_INTERVAL
);