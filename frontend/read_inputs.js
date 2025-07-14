const baseUrl = window.location.origin;

// Reference to the container that holds all sequence blocks
const sequencesContainer = document.getElementById("sequences-container");

// Keep a reference to the original sequence block for cloning
const originalSequenceBlock = sequencesContainer.querySelector(".sequence-block");

// The "Add Another Sequence" button: clones the block & appends it
document.getElementById("add-sequence-btn").addEventListener("click", () => {
	// Clone the original block
	const newBlock = originalSequenceBlock.cloneNode(true);
	// Clear out user input from cloned block
	newBlock.querySelector(".appointment-names").value = "";
	newBlock.querySelector(".start-date").value = "";
	newBlock.querySelector(".end-date").value = "";
	newBlock.querySelector(".interval-days").value = "14";
	// Append to container
	sequencesContainer.appendChild(newBlock);
});

// The "Generate Calendar" button: collects all data & sends POST
document.getElementById("submit-btn").addEventListener("click", async () => {

	const { calendarName, sequences } = collectCalendar();

	// Create the final payload
	const payload = {
		calendar_name: calendarName,
		sequences: sequences
	};

	console.log("Sending Payload:", payload);

	// Send to endpoint
	try {
		const response = await fetch(baseUrl + "/generate_calendar/", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(payload)
		});

		if (response.ok) {
			// Read ICS as a Blob
			const icsBlob = await response.blob();

			// Create a temporary download link in the browser
			const icsURL = URL.createObjectURL(icsBlob);
			const link = document.createElement("a");
			link.href = icsURL;
			link.download = calendarName;
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
			URL.revokeObjectURL(icsURL);
		} else {
			const errorData = await response.text();
			alert("Error generating calendar:\n" + errorData);
		}
	} catch (err) {
		console.error(err);
		alert("Network error or server not reachable.");
	}
});


function collectCalendar() {
	const calendarName = document.getElementById("calendar-name").value || "recurring_appointments.ics";

	// Build the sequences array
	const sequenceBlocks = sequencesContainer.querySelectorAll(".sequence-block");
	const sequences = [];

	sequenceBlocks.forEach(block => {
		const appointmentNames = block.querySelector(".appointment-names").value.split(",").map(s => s.trim());
		const startDate = block.querySelector(".start-date").value;
		const endDate = block.querySelector(".end-date").value;
		const recurrenceIntervalDays = parseInt(block.querySelector(".interval-days").value, 10);

		// Skip empty blocks or invalid data if you want to handle validation
		if (!startDate || !appointmentNames[0]) {
			return;
		}

		sequences.push({
			appointment_names: appointmentNames,
			start_date: startDate,
			end_date: endDate,
			recurrence_interval_days: recurrenceIntervalDays
		});
	});
	return { calendarName, sequences };
}

