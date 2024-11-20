document.addEventListener('DOMContentLoaded', function() {
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.src = document.documentElement.dataset.backgroundImage || "/static/background/images/main_bg.jpg";

    img.onload = function() {
        document.body.style.setProperty('--background-image-url', `url('${img.src}')`);
        document.body.classList.add('background-loaded');
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        try {
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
            let colors = [];

            for(let i = 0; i < imageData.length; i += 200) {
                const r = imageData[i];
                const g = imageData[i + 1];
                const b = imageData[i + 2];

                const brightness = (r + g + b) / 3;
                if(brightness > 30 && brightness < 220) {
                    colors.push([r, g, b]);
                }
            }

            colors.sort((a, b) => {
                const saturationA = Math.max(...a) - Math.min(...a);
                const saturationB = Math.max(...b) - Math.min(...b);
                return saturationB - saturationA;
            });

            const dominantColor = colors[0] || [255, 255, 255];
            const secondaryColor = colors[Math.floor(colors.length / 2)] || [255, 255, 255];

            document.documentElement.style.setProperty(
                '--dominant-color',
                `rgba(${dominantColor[0]}, ${dominantColor[1]}, ${dominantColor[2]}, 0.5)`
            );
            document.documentElement.style.setProperty(
                '--secondary-color',
                `rgba(${secondaryColor[0]}, ${secondaryColor[1]}, ${secondaryColor[2]}, 0.3)`
            );
        } catch(e) {
            document.documentElement.style.setProperty(
                '--dominant-color',
                'rgba(255, 255, 255, 0.3)'
            );
            document.documentElement.style.setProperty(
                '--secondary-color',
                'rgba(255, 255, 255, 0.2)'
            );
        }
    };

    img.onerror = function() {
        document.documentElement.style.setProperty(
            '--dominant-color',
            'rgba(255, 255, 255, 0.3)'
        );
        document.documentElement.style.setProperty(
            '--secondary-color',
            'rgba(255, 255, 255, 0.2)'
        );
    };
});