const CommissionAllocationUI = (() => {
    const formatCurrency = (value) =>
        new Intl.NumberFormat("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }).format(value);

    const parseNumber = (value) => {
        const parsed = Number.parseFloat(value);
        return Number.isFinite(parsed) ? parsed : 0;
    };

    const getElement = (id) => document.getElementById(id);

    const getInputs = () => ({
        saleAmount: getElement("saleAmount"),
        commission: getElement("id_commission_percentage"),
        tds: getElement("id_tds_percentage"),
        deduction: getElement("id_other_deduction"),
        allocationPercents: Array.from(document.querySelectorAll(".allocation-percent")),
        allocationGross: Array.from(document.querySelectorAll(".allocation-gross")),
        allocationTds: Array.from(document.querySelectorAll(".allocation-tds")),
        allocationNet: Array.from(document.querySelectorAll(".allocation-net")),
        grossSummary: getElement("grossCommission"),
        tdsSummary: getElement("tdsAmount"),
        deductionSummary: getElement("otherDeduction"),
        netSummary: getElement("netCommission"),
        allocatedSummary: getElement("allocated"),
        remainingSummary: getElement("remaining"),
        allocationPercentDisplay: getElement("allocationPercentDisplay"),
        allocationBadge: getElement("allocationBadge"),
        generateButton: getElement("generateBtn"),
        totalBadge: getElement("allocationTotalBadge"),
        statusText: getElement("allocationStatusText"),
    });

    const updateAllocationRows = (state, inputs) => {
        let totalPercentage = 0;
        let allocatedAmount = 0;

        inputs.allocationPercents.forEach((input, index) => {
            const percentage = Math.max(0, parseNumber(input.value));
            totalPercentage += percentage;

            const grossShare = state.grossCommission * (percentage / 100);
            const tdsShare = state.tdsAmount * (percentage / 100);
            const netShare = state.netCommission * (percentage / 100);

            if (inputs.allocationGross[index]) {
                inputs.allocationGross[index].value = formatCurrency(grossShare);
            }

            if (inputs.allocationTds[index]) {
                inputs.allocationTds[index].value = formatCurrency(tdsShare);
            }

            if (inputs.allocationNet[index]) {
                inputs.allocationNet[index].value = formatCurrency(netShare);
            }

            allocatedAmount += netShare;
        });

        return {
            totalPercentage,
            allocatedAmount,
            isComplete: Math.abs(totalPercentage - 100) < 0.0001,
        };
    };

    const updateSummary = (state, inputs, allocationResult) => {
        const remainingAmount = state.netCommission - allocationResult.allocatedAmount;
        const remainingPercentage = state.netCommission > 0 ? (remainingAmount / state.netCommission) * 100 : 0;

        if (inputs.totalBadge) {
            inputs.totalBadge.className = `badge rounded-pill fs-6 px-3 py-2 ${allocationResult.isComplete ? "text-bg-success" : "text-bg-danger"}`;
            inputs.totalBadge.textContent = `${allocationResult.totalPercentage.toFixed(2)}%`;
        }

        if (inputs.statusText) {
            inputs.statusText.textContent = allocationResult.isComplete
                ? "Allocation complete"
                : "Adjust allocation to total 100%";
            inputs.statusText.className = `small ${allocationResult.isComplete ? "text-success" : "text-danger"}`;
        }

        if (inputs.grossSummary) {
            inputs.grossSummary.textContent = formatCurrency(state.grossCommission);
        }

        if (inputs.tdsSummary) {
            inputs.tdsSummary.textContent = formatCurrency(state.tdsAmount);
        }

        if (inputs.deductionSummary) {
            inputs.deductionSummary.textContent = formatCurrency(parseNumber(document.getElementById("id_other_deduction")?.value || 0));
        }

        if (inputs.netSummary) {
            inputs.netSummary.textContent = formatCurrency(state.netCommission);
        }

        if (inputs.allocatedSummary) {
            inputs.allocatedSummary.textContent = formatCurrency(allocationResult.allocatedAmount);
        }

        if (inputs.remainingSummary) {
            inputs.remainingSummary.textContent = formatCurrency(remainingPercentage);
        }

        if (inputs.allocationPercentDisplay) {
            inputs.allocationPercentDisplay.textContent = `${allocationResult.totalPercentage.toFixed(2)}%`;
        }

        if (inputs.allocationBadge) {
            inputs.allocationBadge.className = `badge rounded-pill ms-2 ${allocationResult.isComplete ? "text-bg-success" : "text-bg-danger"}`;
            inputs.allocationBadge.textContent = allocationResult.isComplete ? "Complete" : "Pending";
        }

        if (inputs.generateButton) {
            inputs.generateButton.disabled = !allocationResult.isComplete;
        }
    };

    const calculateState = (inputs) => {
        const saleAmount = parseNumber(inputs.saleAmount?.textContent || 0);
        const commissionRate = parseNumber(inputs.commission?.value);
        const tdsRate = parseNumber(inputs.tds?.value);
        const deductionAmount = parseNumber(inputs.deduction?.value);

        const grossCommission = saleAmount * (commissionRate / 100);
        const tdsAmount = grossCommission * (tdsRate / 100);
        const netCommission = grossCommission - tdsAmount - deductionAmount;

        return {
            saleAmount,
            grossCommission,
            tdsAmount,
            netCommission,
        };
    };

    const bindEvents = (inputs) => {
        const refresh = () => {
            const state = calculateState(inputs);
            const allocationResult = updateAllocationRows(state, inputs);
            updateSummary(state, inputs, allocationResult);
        };

        [inputs.commission, inputs.tds, inputs.deduction].forEach((field) => {
            if (field) {
                field.addEventListener("input", refresh);
            }
        });

        inputs.allocationPercents.forEach((input) => {
            input.addEventListener("input", refresh);
        });

        refresh();
    };

    const init = () => {
        const inputs = getInputs();

        if (!inputs.generateButton) {
            return;
        }

        if (inputs.allocationPercents.length === 0) {
            inputs.generateButton.disabled = true;
            return;
        }

        inputs.allocationPercents.forEach((input) => {
            if (!input.value) {
                input.value = (100 / inputs.allocationPercents.length).toFixed(2);
            }
        });

        bindEvents(inputs);
    };

    return { init };
})();

document.addEventListener("DOMContentLoaded", () => {
    CommissionAllocationUI.init();
});
