const fullStatsDiv = document.querySelector('.full-stats');
const outerModal = document.querySelector('.outer-modal');

function showModal() {
  outerModal.style.display = 'block';
  fullStatsDiv.style.display = 'flex';

  // Force reflow before applying transition
  void outerModal.offsetWidth;
  void fullStatsDiv.offsetWidth;

  outerModal.classList.add('show');
  fullStatsDiv.classList.add('show');
}

function hideModal() {
  outerModal.classList.remove('show');
  fullStatsDiv.classList.remove('show');

  outerModal.addEventListener('transitionend', () => {
    outerModal.style.display = 'none';
  }, { once: true });

  fullStatsDiv.addEventListener('transitionend', () => {
    fullStatsDiv.style.display = 'none';
  }, { once: true });
};

function outerModalClick() {
    hideModal();
    document.querySelector('.left-right-buttons').style.display = 'none';
};



function fullStats(characterName) {
    Promise.all([
        fetch(`http://localhost:3000/characters/${characterName}`).then(res => res.json()),
        fetch(`http://localhost:3000/characters/${characterName}/previous`).then(res => res.ok ? res.json() : null),
        fetch(`http://localhost:3000/characters/${characterName}/next`).then(res => res.ok ? res.json() : null),
        fetch("http://localhost:3000/classes").then(res => res.json())
    ])
    .then(([character, previousCharacter, nextCharacter, classes]) => {
        document.querySelector(".content-area").remove();
        window.previousCharacter = previousCharacter;
        window.nextCharacter = nextCharacter;

        const characterInfo = character;
        prevCharacterName = null;
        if (previousCharacter) {
            const prevCharacterName = previousCharacter.name;
        }
        nextCharacterName = null;
        if (nextCharacter) {
            const nextCharacterName = nextCharacter.name;
        }
        
        // get personal skill info
        const personalSkillEntries = Object.entries(characterInfo.personalSkill)
        const [personalSkillName, [personalSkillDescr, personalSkillUrl]] = personalSkillEntries[0];

        // get character classes
        var baseClass = characterInfo.baseClass;
        const promotedOne = characterInfo.promotedClasses[0];
        const promotedTwo = characterInfo.promotedClasses[1];

        const heartSealBase = characterInfo.heartSealBase;
        const heartPromotedOne = characterInfo.heartSealPromoted[0];
        const heartPromotedTwo = characterInfo.heartSealPromoted[1];


        // function that takes a class and outputs class-box div
        function getWeaponRanks(cclass) {
            const classData = classes.find(cls => cls.class === cclass);
            const weaponsContainer = document.createElement("div");
            weaponsContainer.className = "weapon-ranks";
            let html = ``;

            for (const [weapon, rank] of Object.entries(classData.weapons)) {
                html += `
                    <div>
                        <img src="assets/weapons/FE14_${weapon}.png" class="weapon-icon">
                        Max Rank:
                        <div class="weapon-letter">${rank}</div>
                    </div>
                `;
            }
            weaponsContainer.innerHTML = html;
            return weaponsContainer;
        }
        // input: class name -- output: skill-list div
        function getSkillList(cclass) {
            const classData = classes.find(cls => cls.class === cclass);
            const skillsContainer = document.createElement("div");
            skillsContainer.className = "skill-list";
            let html = `
                <div class="skill"> 
                    <div>Personal</div> 
                    <div class="skill-sprite">
                        &#8594; 
                        <img src="${personalSkillUrl}">
                    </div>
                    <div class="skill-description">
                        <div class="skill-name">${personalSkillName}</div>
                        <div>${personalSkillDescr}</div>
                    </div>
                </div>
            `;
            for (const [skillName, skillInfo] of Object.entries(classData.skills)) {
                html += `
                    <div class="skill"> 
                        <div>Lv. ${skillInfo[0]}</div> 
                        <div class="skill-sprite">
                            &#8594; 
                            <img src="${skillInfo[2]}">
                        </div>
                        <div class="skill-description">
                            <div class="skill-name">${skillName}</div>
                            <div>${skillInfo[1]}</div>
                        </div>
                    </div>
                `;
            }
            skillsContainer.innerHTML = html;
            return skillsContainer;
        }
        // input: class name -- output: full-growth-rates div
        function getGrowthRates(cclass) {
            const classData = classes.find(cls => cls.class === cclass);
            const growthRatesContainer = document.createElement("div");
            growthRatesContainer.className = "full-growth-rates";
            let html = ``;

            const characterGrowths = characterInfo.growthRates;
            const classGrowths = classData.classGrowthRates;
            var finalGrowths = [];

            for (const key in characterGrowths) {
                let charGrowth = characterGrowths[key];
                let charNum = parseInt(charGrowth, 10);

                let classGrowth = classGrowths[key];
                let classNum = parseInt(classGrowth, 10);

                let finalNum = charNum + classNum;
                finalGrowths.push(finalNum);
            }
            html += `
                <p>Growth rates</p>
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
                            <td>${finalGrowths[0]}%</td>
                            <td>${finalGrowths[1]}%</td>
                            <td>${finalGrowths[2]}%</td>
                            <td>${finalGrowths[3]}%</td>
                            <td>${finalGrowths[4]}%</td>
                            <td>${finalGrowths[5]}%</td>
                            <td>${finalGrowths[6]}%</td>
                            <td>${finalGrowths[7]}%</td>
                        </tr>
                    </tbody>
                </table>
            `;
            growthRatesContainer.innerHTML = html;
            return growthRatesContainer;
        }
        // input: class name -- output: max-stats div
        function getMaxStats(cclass) {
            const classData = classes.find(cls => cls.class === cclass);
            const maxStatsContainer = document.createElement("div");
            maxStatsContainer.className = "max-stats";
            let html = ``;

            const characterMaxes = characterInfo.maxStats;
            const classMaxes = classData.classMaxStats;
            var finalMaxes = {};

            for (const key in characterMaxes) {
                let charMax = characterMaxes[key];
                let charNum = parseInt(charMax, 10);

                realKey = key;
                if (key === "Luk") {
                    realKey = "Lck";
                }
                let classMax = classMaxes[realKey];
                let classNum = parseInt(classMax, 10);

                let finalNum = charNum + classNum;
                finalMaxes[realKey] = finalNum;
            }
            html += `
                <p>Max stats</p>
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
                            <td>${classMaxes["HP"]}</td>
                            <td>${finalMaxes["Str"]}</td>
                            <td>${finalMaxes["Mag"]}</td>
                            <td>${finalMaxes["Skl"]}</td>
                            <td>${finalMaxes["Spd"]}</td>
                            <td>${finalMaxes["Lck"]}</td>
                            <td>${finalMaxes["Def"]}</td>
                            <td>${finalMaxes["Res"]}</td>
                            <td>${classMaxes["Mov"]}</td>
                        </tr>
                    </tbody>
                </table>
            `;
            maxStatsContainer.innerHTML = html;
            return maxStatsContainer;
        }

        // create and return class-box div
        function createClassBox(cclass) {
            const classBox = document.createElement("div");
            classBox.className = "class-box";
            let html = `
                <h1 class="class-title">
                    <img src="assets/sprites/${characterName}-${cclass}.gif" class="sprite">
                    <div>${cclass}</div>
                </h1>
            `;
            classBox.innerHTML = html;
            classBox.appendChild(getWeaponRanks(cclass));
            classBox.appendChild(getSkillList(cclass));
            classBox.appendChild(getGrowthRates(cclass));
            classBox.appendChild(getMaxStats(cclass));
            return classBox;
        }
        

        const container = document.querySelector(".full-stats");
        const contentArea = document.createElement("div");
        contentArea.className = "content-area";
        html = `
            <!-- Character Portrait and Name -->
            <section class="character-panel">
                <img src="assets/fullsize/${characterName}-fullsize.webp" class="character-fullsize">
                <h1 class="character-name">${characterName}</h1>
            </section>

            <!-- All Class Information -->
            <section class="class-info-panel">
                <div class="heart-seal">
                    Heart Seal
                </div>

                <div class="class-cards"></div>
            </section>
        `
        contentArea.innerHTML = html;

        const heartSealContainer = contentArea.querySelector(".heart-seal");
        const heartCheckbox = document.createElement("input");
        heartCheckbox.type = "checkbox";
        heartCheckbox.id = "heart-seal-check";
        heartCheckbox.checked = false;

        // check if heartSeal is checked or nah
        heartCheckbox.addEventListener("change", heartToggle);

        function heartToggle () {
            document.querySelector(".class-cards").innerHTML = ``;
            if (!heartCheckbox.checked) { // Default Classes
                const CardsContainer = document.querySelector(".class-cards");
                if (baseClass) { // fill in baseClass class-box
                    let html = `
                        <div class="base">
                            Base Class
                        </div>
                    `;
                    CardsContainer.innerHTML += html;
                    const base = CardsContainer.querySelector(".base");
                    base.appendChild(createClassBox(baseClass));
                }

                if (promotedOne || promotedTwo) {
                    let html = `
                        <div class="promotions">
                            Class Promotions
                            <div class="promotion-boxes"></div>
                        </div>
                    `;
                    CardsContainer.innerHTML += html;
                    if (promotedOne) {
                        const promotions = CardsContainer.querySelector(".promotion-boxes");
                        promotions.appendChild(createClassBox(promotedOne));
                    };
                    if (promotedTwo) {
                        const promotions = CardsContainer.querySelector(".promotion-boxes");
                        promotions.appendChild(createClassBox(promotedTwo));
                    };
                }
            } else { // Heart Seal Classes
                const CardsContainer = document.querySelector(".class-cards");
                if (heartSealBase) {
                    let html = `
                        <div class="base">
                            Base Class
                        </div>
                    `;
                    CardsContainer.innerHTML += html;
                    const base = CardsContainer.querySelector(".base");
                    base.appendChild(createClassBox(heartSealBase));
                }

                if (heartPromotedOne || heartPromotedTwo) {
                    let html = `
                        <div class="promotions">
                            Class Promotions
                            <div class="promotion-boxes"></div>
                        </div>
                    `;
                    CardsContainer.innerHTML += html;
                    if (heartPromotedOne) {
                        const promotions = CardsContainer.querySelector(".promotion-boxes");
                        promotions.appendChild(createClassBox(heartPromotedOne));
                    };
                    if (heartPromotedTwo) {
                        const promotions = CardsContainer.querySelector(".promotion-boxes");
                        promotions.appendChild(createClassBox(heartPromotedTwo));
                    };
                }

                console.log("Checkbox is checked!");
            }
        };
        heartSealContainer.appendChild(heartCheckbox);
        container.appendChild(contentArea);
        heartToggle();

        showModal();
        document.querySelector('.left-right-buttons').style.display = 'flex';

        leftButton = document.querySelector('.left');
        rightButton = document.querySelector('.right');
        leftButton.addEventListener("click", () =>prevStats(prevCharacterName));
        rightButton.addEventListener("click", () =>nextStats(nextCharacterName));
    })
};

function prevStats(previousCharacter) {
    if (!previousCharacter) {
        return;
    }
    fullStats(previousCharacter);
};

function nextStats(nextCharacter) {
    if (!nextCharacter) {
        return;
    }
    fullStats(nextCharacter);
};

const pressedClass = "button-pressed";

function pressButton(button) {
    if (!button) return;
    button.classList.add(pressedClass);
    setTimeout(() => button.classList.remove(pressedClass), 100);
}

document.addEventListener("keydown", (event) => {
    if (["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) return;
    if (event.key === "ArrowLeft" || event.key === "<") {
        if (window.previousCharacter?.name) {
            pressButton(document.querySelector('.left'));
            prevStats(previousCharacter.name);
        }
    } else if (event.key === "ArrowRight" || event.key === ">") {
        if (window.nextCharacter?.name) {
            pressButton(document.querySelector('.right'));
            nextStats(nextCharacter.name);
        }
    }
});

