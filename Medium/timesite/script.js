// Arcade Time-Lock Logic

function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toTimeString().split(' ')[0];
    
    const hours = now.getHours();
    const minutes = now.getMinutes();
    
    // Check for 12, 15, 18, 21 hours during minute 0
    const targetHours = [12, 15, 18, 21];
    
    if (targetHours.includes(hours) && minutes === 0) {
        unlockVault();
    } else {
        document.getElementById('lock-status').innerText = "STATUS: VAULT LOCKED";
        document.getElementById('flag-display').innerText = "=== ACCESS DENIED ===";
    }
}

// Hidden function players can find or run in browser console
function unlockVault() {
    // Obfuscated string array for flag: IITMCC{T1M3_W41T5_F0R_N0_1}
    const b1 = "IITMCC{T1M3_";
    const b2 = "W41T5_F0R_";
    const b3 = "N0_1}";
    
    const flag = b1 + b2 + b3;
    
    document.getElementById('lock-status').innerText = "STATUS: VAULT UNLOCKED";
    document.getElementById('flag-display').innerText = flag;
    return flag;
}

setInterval(updateClock, 1000);