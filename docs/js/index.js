
Promise.all([
  fetch(`${API_BASE_URL}/characters`).then(res => res.json()),
  fetch(`${API_BASE_URL}/classes`).then(res => res.json())
])
.then(([characters, classes]) => {
  characters.forEach(character => {
    const name = character.name;
    var char_class = character.class;
    const level = character.startLevel;
    const baseStats = character.baseStats;
    var growthRates = character.growthRates;
    const sprites = character.sprites
    const class_sprite = sprites[char_class]

    const startClassData = classes.find(cls => cls.class === char_class);
    char_class = character.class;

    const container = document.querySelector(".character-cards");
    const card = document.createElement("div");
    card.className = "card";
    card.addEventListener("click", () => fullStats(name));

    html = `
      <img src="assets/FatesPortraits/${name}.png" class="portrait">
      <div class="name">${name}</div>
      <div class="classes">
          <div>${char_class}</div> <div>|</div> <div>Lv. ${level}</div> <div>|</div>
    `
    const entries = Object.entries(character.personalSkill);
    const [skillName, [description, iconUrl]] = entries[0];

    if (startClassData && startClassData.weapons) {
        for (const [weapon, rank] of Object.entries(startClassData.weapons)) {
        html += `
            <img src="assets/weapons/FE14_${weapon}.png" class="weapon-icon">
        `;
        }
    }
    
    // update every number in growthRates here
    for (const key in growthRates) {
        let baseGrowthRate = growthRates[key];
        let valueNum = parseInt(baseGrowthRate, 10);

        // get the class growth rate
        let classGrowthRate = startClassData.classGrowthRates[key]
        let classNum = parseInt(classGrowthRate, 10);

        // calculate and input combined growth rate
        let finalGrowthRate = valueNum + classNum;
        growthRates[key] = finalGrowthRate + "";
    }

    html += `
      </div>
      </div>
      <div class="base-stats">
          <div>Base stats:</div>
          <table>
              <thead>
                  <tr>
                      <td>HP</td>
                      <td>Str</td>
                      <td>Mag</td>
                      <td>Skl</td>
                      <td>Spd</td>
                      <td>Lck</td>
                      <td>Def</td>
                      <td>Res</td>
                      <td>Mov</td>
                  </tr>
              </thead>
              
              <tbody>
                  <tr>
                      <td>${baseStats["HP"]}</td>
                      <td>${baseStats["Str"]}</td>
                      <td>${baseStats["Mag"]}</td>
                      <td>${baseStats["Skl"]}</td>
                      <td>${baseStats["Spd"]}</td>
                      <td>${baseStats["Lck"]}</td>
                      <td>${baseStats["Def"]}</td>
                      <td>${baseStats["Res"]}</td>
                      <td>${baseStats["Mov"]}</td>
                  </tr>
              </tbody>
          </table>
      </div>
      <div class="growth-rates">
          <div>Growth rates:</div>
          <table>
              <thead>
                  <tr>
                      <td>HP</td>
                      <td>Str</td>
                      <td>Mag</td>
                      <td>Skl</td>
                      <td>Spd</td>
                      <td>Lck</td>
                      <td>Def</td>
                      <td>Res</td>
                  </tr>
              </thead>
              <tbody>
                  <tr>
                      <td>${growthRates["HP"]}%</td>
                      <td>${growthRates["Str"]}%</td>
                      <td>${growthRates["Mag"]}%</td>
                      <td>${growthRates["Skl"]}%</td>
                      <td>${growthRates["Spd"]}%</td>
                      <td>${growthRates["Lck"]}%</td>
                      <td>${growthRates["Def"]}%</td>
                      <td>${growthRates["Res"]}%</td>
                  </tr>
              </tbody>
          </table>
      </div>
    `;

    card.innerHTML = html
    container.appendChild(card);
  });


  
})
.catch(error => {
  console.error("Error fetching characters:", error)
});

