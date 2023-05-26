const chords = ["N", "Dm", "Bb", "F", "Dm7", "Bb", "F", "Dm7", "Bb", "F", "Dm7", "Bb", "F", "Bb", "F", "Bb", "F", "C", "C7", "F", "Bb", "F", "C", "Dm7", "Bbmaj7", "F", "Dm7", "Bb", "F", "Dm7", "Bbmaj7", "F", "Dm", "Bbmaj7", "F", "C6", "Bb", "F", "Bb", "F", "C", "C7", "F", "Bb", "F", "Dm", "Bb", "F", "Dm", "Bbmaj7", "F", "Dm", "Bbmaj7", "F", "Dm7", "Bbmaj7", "F", "Dm7", "Bb", "F"];
const duracao = [93, 3251, 2972, 6873, 3529, 2879, 6687, 3251, 2972, 6873, 3344, 2972, 6780, 6223, 6873, 6037, 7059, 4087, 2508, 3158, 3344, 5759, 743, 3529, 2972, 6687, 3344, 3251, 6502, 3344, 3158, 6594, 3344, 3158, 5108, 1486, 6594, 6594, 6316, 6873, 3622, 2786, 3251, 3437, 6409, 3344, 3344, 6594, 3065, 3437, 6502, 3251, 3344, 6409, 3251, 3529, 6409, 3251, 3344, 9567];

const chordBox = document.getElementById('chord-box');
const audioPlayer = document.getElementById('audio-player');
const playButton = document.getElementById('play-button');

let interval;

function showChord(index) {
  const containerWidth = chordBox.parentElement.clientWidth;
  const spacing = (containerWidth - chordBox.clientWidth) / (chords.length - 1);

  chordBox.style.left = `${index * spacing}px`;
  chordBox.innerText = chords[index];
}

function playTimeline() {
  let index = 0;

  function playNextChord() {
    showChord(index);
    index++;

    if (index >= chords.length) {
      clearInterval(interval);
      return;
    }

    interval = setTimeout(playNextChord, duracao[index]);
  }

  playNextChord();
}

function playAudio() {
  audioPlayer.play();
}

playButton.addEventListener('click', () => {
  playTimeline();
  playAudio();
});
