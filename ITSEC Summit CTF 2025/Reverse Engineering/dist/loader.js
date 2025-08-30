    try {
        nw.Window.get().evalNWBin(null, 'app.bin');
    } catch (error) {
        console.error('Failed to load binary:', error);
    }