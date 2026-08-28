from datetime import datetime

VERSES = [

    # Day 1
    ("Genesis 1:1", "In the beginning God created the heaven and the earth."),

    # Day 2
    ("Genesis 1:27", "So God created man in His own image, in the image of God created He him."),

    # Day 3
    ("Genesis 12:2", "I will make of thee a great nation, and I will bless thee."),

    # Day 4
    ("Exodus 14:14", "The Lord shall fight for you, and ye shall hold your peace."),

    # Day 5
    ("Deuteronomy 31:6", "Be strong and of a good courage, fear not, for the Lord thy God is with thee."),

    # Day 6
    ("Joshua 1:9", "Be strong and courageous; be not afraid, for the Lord thy God is with thee wherever thou goest."),

    # Day 7
    ("Joshua 24:15", "Choose you this day whom ye will serve; but as for me and my house, we will serve the Lord."),

    # Day 8
    ("1 Samuel 16:7", "The Lord looketh on the heart."),

    # Day 9
    ("2 Samuel 22:31", "As for God, His way is perfect."),

    # Day 10
    ("1 Kings 8:61", "Let your heart therefore be perfect with the Lord our God."),

    # Day 11
    ("2 Chronicles 7:14", "If My people shall humble themselves, and pray, and seek My face."),

    # Day 12
    ("Nehemiah 8:10", "The joy of the Lord is your strength."),

    # Day 13
    ("Job 19:25", "For I know that my Redeemer liveth."),

    # Day 14
    ("Psalm 1:1", "Blessed is the man that walketh not in the counsel of the ungodly."),

    # Day 15
    ("Psalm 23:1", "The Lord is my shepherd; I shall not want."),

    # Day 16
    ("Psalm 27:1", "The Lord is my light and my salvation; whom shall I fear?"),

    # Day 17
    ("Psalm 34:8", "O taste and see that the Lord is good."),

    # Day 18
    ("Psalm 37:4", "Delight thyself also in the Lord."),

    # Day 19
    ("Psalm 46:1", "God is our refuge and strength, a very present help in trouble."),

    # Day 20
    ("Psalm 46:10", "Be still, and know that I am God."),

    # Day 21
    ("Psalm 51:10", "Create in me a clean heart, O God."),

    # Day 22
    ("Psalm 91:1", "He that dwelleth in the secret place of the Most High shall abide under the shadow of the Almighty."),

    # Day 23
    ("Psalm 100:5", "The Lord is good; His mercy is everlasting."),

    # Day 24
    ("Psalm 103:2", "Bless the Lord, O my soul, and forget not all His benefits."),

    # Day 25
    ("Psalm 119:105", "Thy word is a lamp unto my feet, and a light unto my path."),

    # Day 26
    ("Proverbs 3:5-6", "Trust in the Lord with all thine heart; and lean not unto thine own understanding."),

    # Day 27
    ("Proverbs 16:3", "Commit thy works unto the Lord."),

    # Day 28
    ("Proverbs 18:10", "The name of the Lord is a strong tower."),

    # Day 29
    ("Ecclesiastes 3:1", "To every thing there is a season."),

    # Day 30
    ("Isaiah 40:31", "They that wait upon the Lord shall renew their strength."),    # Day 31
    ("Isaiah 41:10", "Fear thou not; for I am with thee: be not dismayed; for I am thy God."),

    # Day 32
    ("Isaiah 43:2", "When thou passest through the waters, I will be with thee."),

    # Day 33
    ("Jeremiah 17:7", "Blessed is the man that trusteth in the Lord, and whose hope the Lord is."),

    # Day 34
    ("Jeremiah 29:11", "For I know the thoughts that I think toward you, saith the Lord, thoughts of peace."),

    # Day 35
    ("Lamentations 3:22-23", "It is of the Lord's mercies that we are not consumed, because His compassions fail not."),

    # Day 36
    ("Ezekiel 36:26", "A new heart also will I give you, and a new spirit will I put within you."),

    # Day 37
    ("Daniel 3:17", "Our God whom we serve is able to deliver us."),

    # Day 38
    ("Hosea 6:6", "For I desired mercy, and not sacrifice; and the knowledge of God more than burnt offerings."),

    # Day 39
    ("Joel 2:25", "I will restore to you the years that the locust hath eaten."),

    # Day 40
    ("Amos 5:24", "But let judgment run down as waters, and righteousness as a mighty stream."),

    # Day 41
    ("Micah 6:8", "He hath shewed thee, O man, what is good; and what doth the Lord require of thee."),

    # Day 42
    ("Nahum 1:7", "The Lord is good, a strong hold in the day of trouble."),

    # Day 43
    ("Habakkuk 2:4", "The just shall live by his faith."),

    # Day 44
    ("Zephaniah 3:17", "The Lord thy God in the midst of thee is mighty; He will save."),

    # Day 45
    ("Zechariah 4:6", "Not by might, nor by power, but by My spirit, saith the Lord."),

    # Day 46
    ("Malachi 3:10", "Bring ye all the tithes into the storehouse."),

    # Day 47
    ("Matthew 5:14", "Ye are the light of the world."),

    # Day 48
    ("Matthew 5:16", "Let your light so shine before men, that they may see your good works."),

    # Day 49
    ("Matthew 6:33", "Seek ye first the kingdom of God, and His righteousness."),

    # Day 50
    ("Matthew 7:7", "Ask, and it shall be given you; seek, and ye shall find."),

    # Day 51
    ("Matthew 11:28", "Come unto Me, all ye that labour and are heavy laden, and I will give you rest."),

    # Day 52
    ("Matthew 19:26", "With God all things are possible."),

    # Day 53
    ("Matthew 22:37", "Thou shalt love the Lord thy God with all thy heart."),

    # Day 54
    ("Matthew 28:19", "Go ye therefore, and teach all nations."),

    # Day 55
    ("Mark 9:23", "If thou canst believe, all things are possible to him that believeth."),

    # Day 56
    ("Mark 10:27", "With God all things are possible."),

    # Day 57
    ("Luke 1:37", "For with God nothing shall be impossible."),

    # Day 58
    ("Luke 6:31", "As ye would that men should do to you, do ye also to them likewise."),

    # Day 59
    ("John 3:16", "For God so loved the world, that He gave His only begotten Son."),

    # Day 60
    ("John 8:12", "I am the light of the world: he that followeth Me shall have the light of life."),    # Day 61
    ("John 10:10", "I am come that they might have life, and that they might have it more abundantly."),

    # Day 62
    ("John 11:25", "I am the resurrection, and the life: he that believeth in Me, though he were dead, yet shall he live."),

    # Day 63
    ("John 14:1", "Let not your heart be troubled: ye believe in God, believe also in Me."),

    # Day 64
    ("John 14:6", "I am the way, the truth, and the life: no man cometh unto the Father, but by Me."),

    # Day 65
    ("John 14:27", "Peace I leave with you, My peace I give unto you."),

    # Day 66
    ("Acts 1:8", "Ye shall receive power, after that the Holy Ghost is come upon you."),

    # Day 67
    ("Acts 2:17", "I will pour out of My Spirit upon all flesh."),

    # Day 68
    ("Acts 4:12", "Neither is there salvation in any other: for there is none other name under heaven given among men, whereby we must be saved."),

    # Day 69
    ("Acts 16:31", "Believe on the Lord Jesus Christ, and thou shalt be saved."),

    # Day 70
    ("Romans 1:16", "For I am not ashamed of the gospel of Christ: for it is the power of God unto salvation."),

    # Day 71
    ("Romans 5:8", "God commendeth His love toward us, in that, while we were yet sinners, Christ died for us."),

    # Day 72
    ("Romans 8:1", "There is therefore now no condemnation to them which are in Christ Jesus."),

    # Day 73
    ("Romans 8:28", "All things work together for good to them that love God."),

    # Day 74
    ("Romans 8:31", "If God be for us, who can be against us?"),

    # Day 75
    ("Romans 10:9", "If thou shalt confess with thy mouth the Lord Jesus, and shalt believe in thine heart that God raised Him from the dead, thou shalt be saved."),

    # Day 76
    ("Romans 12:2", "Be transformed by the renewing of your mind."),

    # Day 77
    ("Romans 12:12", "Rejoicing in hope; patient in tribulation; continuing instant in prayer."),

    # Day 78
    ("Romans 12:21", "Be not overcome of evil, but overcome evil with good."),

    # Day 79
    ("1 Corinthians 10:13", "God is faithful, who will not suffer you to be tempted above that ye are able."),

    # Day 80
    ("1 Corinthians 13:4", "Charity suffereth long, and is kind."),

    # Day 81
    ("1 Corinthians 13:13", "Now abideth faith, hope, charity, these three; but the greatest of these is charity."),

    # Day 82
    ("1 Corinthians 15:58", "Be ye stedfast, unmoveable, always abounding in the work of the Lord."),

    # Day 83
    ("2 Corinthians 5:7", "For we walk by faith, not by sight."),

    # Day 84
    ("2 Corinthians 5:17", "If any man be in Christ, he is a new creature."),

    # Day 85
    ("2 Corinthians 9:7", "God loveth a cheerful giver."),

    # Day 86
    ("2 Corinthians 12:9", "My grace is sufficient for thee: for My strength is made perfect in weakness."),

    # Day 87
    ("Galatians 2:20", "I live by the faith of the Son of God, who loved me, and gave Himself for me."),

    # Day 88
    ("Galatians 5:22", "The fruit of the Spirit is love, joy, peace, longsuffering, gentleness, goodness, faith."),

    # Day 89
    ("Galatians 6:9", "Let us not be weary in well doing: for in due season we shall reap."),

    # Day 90
    ("Ephesians 2:8", "For by grace are ye saved through faith; and that not of yourselves: it is the gift of God."),    # Day 91
    ("Ephesians 3:20", "God is able to do exceeding abundantly above all that we ask or think."),

    # Day 92
    ("Ephesians 4:32", "Be ye kind one to another, tenderhearted, forgiving one another."),

    # Day 93
    ("Ephesians 6:10", "Be strong in the Lord, and in the power of His might."),

    # Day 94
    ("Philippians 1:6", "He which hath begun a good work in you will perform it until the day of Jesus Christ."),

    # Day 95
    ("Philippians 4:4", "Rejoice in the Lord alway: and again I say, Rejoice."),

    # Day 96
    ("Philippians 4:6", "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God."),

    # Day 97
    ("Philippians 4:7", "The peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus."),

    # Day 98
    ("Philippians 4:13", "I can do all things through Christ which strengtheneth me."),

    # Day 99
    ("Colossians 3:2", "Set your affection on things above, not on things on the earth."),

    # Day 100
    ("Colossians 3:23", "Whatsoever ye do, do it heartily, as to the Lord."),

    # Day 101
    ("1 Thessalonians 5:16", "Rejoice evermore."),

    # Day 102
    ("1 Thessalonians 5:17", "Pray without ceasing."),

    # Day 103
    ("1 Thessalonians 5:18", "In every thing give thanks: for this is the will of God."),

    # Day 104
    ("2 Thessalonians 3:3", "The Lord is faithful, who shall stablish you, and keep you from evil."),

    # Day 105
    ("1 Timothy 4:12", "Let no man despise thy youth; but be thou an example of the believers."),

    # Day 106
    ("1 Timothy 6:12", "Fight the good fight of faith, lay hold on eternal life."),

    # Day 107
    ("2 Timothy 1:7", "God hath not given us the spirit of fear; but of power, and of love, and of a sound mind."),

    # Day 108
    ("2 Timothy 2:15", "Study to shew thyself approved unto God."),

    # Day 109
    ("2 Timothy 3:16", "All scripture is given by inspiration of God, and is profitable for doctrine."),

    # Day 110
    ("Hebrews 4:12", "The word of God is quick, and powerful, and sharper than any twoedged sword."),

    # Day 111
    ("Hebrews 4:16", "Let us come boldly unto the throne of grace, that we may obtain mercy."),

    # Day 112
    ("Hebrews 10:23", "Let us hold fast the profession of our faith without wavering; for He is faithful that promised."),

    # Day 113
    ("Hebrews 11:1", "Faith is the substance of things hoped for, the evidence of things not seen."),

    # Day 114
    ("Hebrews 11:6", "Without faith it is impossible to please Him."),

    # Day 115
    ("Hebrews 12:1", "Let us run with patience the race that is set before us."),

    # Day 116
    ("Hebrews 13:8", "Jesus Christ the same yesterday, and to day, and for ever."),

    # Day 117
    ("James 1:5", "If any of you lack wisdom, let him ask of God, that giveth to all men liberally."),

    # Day 118
    ("James 1:17", "Every good gift and every perfect gift is from above."),

    # Day 119
    ("James 2:17", "Faith, if it hath not works, is dead, being alone."),

    # Day 120
    ("James 4:8", "Draw nigh to God, and He will draw nigh to you."),    # Day 121
    ("James 5:16", "The effectual fervent prayer of a righteous man availeth much."),

    # Day 122
    ("1 Peter 1:3", "According to His abundant mercy hath begotten us again unto a lively hope."),

    # Day 123
    ("1 Peter 2:9", "Ye are a chosen generation, a royal priesthood, an holy nation, a peculiar people."),

    # Day 124
    ("1 Peter 5:7", "Casting all your care upon Him; for He careth for you."),

    # Day 125
    ("1 Peter 5:10", "The God of all grace, who hath called us unto His eternal glory by Christ Jesus, make you perfect."),

    # Day 126
    ("2 Peter 1:3", "His divine power hath given unto us all things that pertain unto life and godliness."),

    # Day 127
    ("2 Peter 3:9", "The Lord is not slack concerning His promise, but is longsuffering to us-ward."),

    # Day 128
    ("1 John 1:9", "If we confess our sins, He is faithful and just to forgive us our sins."),

    # Day 129
    ("1 John 3:1", "Behold, what manner of love the Father hath bestowed upon us."),

    # Day 130
    ("1 John 4:7", "Let us love one another: for love is of God."),

    # Day 131
    ("1 John 4:19", "We love Him, because He first loved us."),

    # Day 132
    ("1 John 5:14", "This is the confidence that we have in Him, that, if we ask anything according to His will, He heareth us."),

    # Day 133
    ("2 John 1:6", "This is love, that we walk after His commandments."),

    # Day 134
    ("Jude 1:20", "Building up yourselves on your most holy faith, praying in the Holy Ghost."),

    # Day 135
    ("Revelation 1:8", "I am Alpha and Omega, the beginning and the ending, saith the Lord."),

    # Day 136
    ("Revelation 3:20", "Behold, I stand at the door, and knock."),

    # Day 137
    ("Revelation 21:4", "God shall wipe away all tears from their eyes; and there shall be no more sorrow."),

    # Day 138
    ("Psalm 121:1-2", "My help cometh from the Lord, which made heaven and earth."),

    # Day 139
    ("Psalm 118:24", "This is the day which the Lord hath made; we will rejoice and be glad in it."),

    # Day 140
    ("Psalm 119:11", "Thy word have I hid in mine heart, that I might not sin against Thee."),

    # Day 141
    ("Psalm 138:8", "The Lord will perfect that which concerneth me."),

    # Day 142
    ("Psalm 147:3", "He healeth the broken in heart, and bindeth up their wounds."),

    # Day 143
    ("Psalm 150:6", "Let every thing that hath breath praise the Lord."),

    # Day 144
    ("Proverbs 4:23", "Keep thy heart with all diligence; for out of it are the issues of life."),

    # Day 145
    ("Proverbs 10:12", "Hatred stirreth up strifes: but love covereth all sins."),

    # Day 146
    ("Proverbs 11:25", "The liberal soul shall be made fat: and he that watereth shall be watered also himself."),

    # Day 147
    ("Proverbs 15:1", "A soft answer turneth away wrath."),

    # Day 148
    ("Proverbs 16:9", "A man's heart deviseth his way: but the Lord directeth his steps."),

    # Day 149
    ("Proverbs 17:17", "A friend loveth at all times."),

    # Day 150
    ("Proverbs 19:21", "There are many devices in a man's heart; nevertheless the counsel of the Lord shall stand."),    # Day 151
    ("Proverbs 22:6", "Train up a child in the way he should go: and when he is old, he will not depart from it."),

    # Day 152
    ("Proverbs 27:17", "Iron sharpeneth iron; so a man sharpeneth the countenance of his friend."),

    # Day 153
    ("Isaiah 26:3", "Thou wilt keep him in perfect peace, whose mind is stayed on Thee."),

    # Day 154
    ("Isaiah 30:21", "Thine ears shall hear a word behind thee, saying, This is the way, walk ye in it."),

    # Day 155
    ("Isaiah 33:2", "O Lord, be gracious unto us; we have waited for Thee."),

    # Day 156
    ("Isaiah 35:4", "Be strong, fear not: behold, your God will come with vengeance, even God with a recompence."),

    # Day 157
    ("Isaiah 54:17", "No weapon that is formed against thee shall prosper."),

    # Day 158
    ("Jeremiah 1:8", "Be not afraid of their faces: for I am with thee to deliver thee, saith the Lord."),

    # Day 159
    ("Jeremiah 33:3", "Call unto Me, and I will answer thee, and shew thee great and mighty things."),

    # Day 160
    ("Ezekiel 11:19", "I will give them one heart, and I will put a new spirit within you."),

    # Day 161
    ("Daniel 6:23", "No manner of hurt was found upon him, because he believed in his God."),

    # Day 162
    ("Matthew 4:4", "Man shall not live by bread alone, but by every word that proceedeth out of the mouth of God."),

    # Day 163
    ("Matthew 5:9", "Blessed are the peacemakers: for they shall be called the children of God."),

    # Day 164
    ("Matthew 6:34", "Take therefore no thought for the morrow: for the morrow shall take thought for the things of itself."),

    # Day 165
    ("Matthew 18:20", "Where two or three are gathered together in My name, there am I in the midst of them."),

    # Day 166
    ("Matthew 22:39", "Thou shalt love thy neighbour as thyself."),

    # Day 167
    ("Matthew 25:21", "Well done, thou good and faithful servant."),

    # Day 168
    ("Mark 11:24", "What things soever ye desire, when ye pray, believe that ye receive them."),

    # Day 169
    ("Luke 9:23", "If any man will come after Me, let him deny himself, and take up his cross daily, and follow Me."),

    # Day 170
    ("Luke 11:9", "Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you."),

    # Day 171
    ("Luke 12:32", "Fear not, little flock; for it is your Father's good pleasure to give you the kingdom."),

    # Day 172
    ("Luke 18:27", "The things which are impossible with men are possible with God."),

    # Day 173
    ("John 1:5", "The light shineth in darkness; and the darkness comprehended it not."),

    # Day 174
    ("John 15:5", "I am the vine, ye are the branches: he that abideth in Me, bringeth forth much fruit."),

    # Day 175
    ("John 16:33", "In the world ye shall have tribulation: but be of good cheer; I have overcome the world."),

    # Day 176
    ("Acts 20:24", "None of these things move me, neither count I my life dear unto myself."),

    # Day 177
    ("Romans 15:13", "The God of hope fill you with all joy and peace in believing."),

    # Day 178
    ("1 Corinthians 16:14", "Let all your things be done with charity."),

    # Day 179
    ("2 Corinthians 4:16", "Though our outward man perish, yet the inward man is renewed day by day."),

    # Day 180
    ("Galatians 5:25", "If we live in the Spirit, let us also walk in the Spirit."),    # Day 181
    ("Ephesians 1:3", "Blessed be the God and Father of our Lord Jesus Christ, who hath blessed us with all spiritual blessings."),

    # Day 182
    ("Ephesians 2:10", "We are His workmanship, created in Christ Jesus unto good works."),

    # Day 183
    ("Ephesians 5:8", "Walk as children of light."),

    # Day 184
    ("Philippians 2:5", "Let this mind be in you, which was also in Christ Jesus."),

    # Day 185
    ("Philippians 3:14", "I press toward the mark for the prize of the high calling of God in Christ Jesus."),

    # Day 186
    ("Colossians 1:16", "By Him were all things created, that are in heaven, and that are in earth."),

    # Day 187
    ("Colossians 2:6", "As ye have therefore received Christ Jesus the Lord, so walk ye in Him."),

    # Day 188
    ("Colossians 4:2", "Continue in prayer, and watch in the same with thanksgiving."),

    # Day 189
    ("1 Thessalonians 4:7", "God hath not called us unto uncleanness, but unto holiness."),

    # Day 190
    ("1 Thessalonians 5:11", "Comfort yourselves together, and edify one another."),

    # Day 191
    ("2 Thessalonians 2:16-17", "Comfort your hearts, and stablish you in every good word and work."),

    # Day 192
    ("1 Timothy 1:17", "Now unto the King eternal, immortal, invisible, the only wise God, be honour and glory."),

    # Day 193
    ("1 Timothy 6:6", "Godliness with contentment is great gain."),

    # Day 194
    ("2 Timothy 4:7", "I have fought a good fight, I have finished my course, I have kept the faith."),

    # Day 195
    ("Titus 3:5", "Not by works of righteousness which we have done, but according to His mercy He saved us."),

    # Day 196
    ("Philemon 1:6", "That the communication of thy faith may become effectual."),

    # Day 197
    ("Hebrews 6:19", "Which hope we have as an anchor of the soul, both sure and stedfast."),

    # Day 198
    ("Hebrews 10:35", "Cast not away therefore your confidence, which hath great recompence of reward."),

    # Day 199
    ("Hebrews 13:5", "I will never leave thee, nor forsake thee."),

    # Day 200
    ("James 3:17", "The wisdom that is from above is first pure, then peaceable, gentle, and easy to be entreated."),

    # Day 201
    ("1 Peter 3:8", "Be ye all of one mind, having compassion one of another, love as brethren."),

    # Day 202
    ("1 Peter 4:8", "Above all things have fervent charity among yourselves: for charity shall cover the multitude of sins."),

    # Day 203
    ("2 Peter 1:5", "Add to your faith virtue; and to virtue knowledge."),

    # Day 204
    ("1 John 2:17", "He that doeth the will of God abideth for ever."),

    # Day 205
    ("1 John 4:18", "Perfect love casteth out fear."),

    # Day 206
    ("Jude 1:24", "Unto Him that is able to keep you from falling, and to present you faultless before His presence."),

    # Day 207
    ("Revelation 2:10", "Be thou faithful unto death, and I will give thee a crown of life."),

    # Day 208
    ("Revelation 3:5", "He that overcometh shall be clothed in white raiment."),

    # Day 209
    ("Revelation 5:13", "Blessing, and honour, and glory, and power, be unto Him that sitteth upon the throne."),

    # Day 210
    ("Revelation 22:12", "Behold, I come quickly; and My reward is with Me, to give every man according as his work shall be."),    # Day 211
    ("Genesis 15:1", "Fear not, Abram: I am thy shield, and thy exceeding great reward."),

    # Day 212
    ("Genesis 22:17", "In blessing I will bless thee, and in multiplying I will multiply thy seed."),

    # Day 213
    ("Exodus 15:2", "The Lord is my strength and song, and He is become my salvation."),

    # Day 214
    ("Exodus 20:3", "Thou shalt have no other gods before Me."),

    # Day 215
    ("Leviticus 19:18", "Thou shalt love thy neighbour as thyself."),

    # Day 216
    ("Numbers 6:24-26", "The Lord bless thee, and keep thee: the Lord make His face shine upon thee."),

    # Day 217
    ("Deuteronomy 6:5", "Thou shalt love the Lord thy God with all thine heart, and with all thy soul."),

    # Day 218
    ("Deuteronomy 7:9", "Know therefore that the Lord thy God, He is God, the faithful God."),

    # Day 219
    ("Joshua 23:8", "But cleave unto the Lord your God, as ye have done unto this day."),

    # Day 220
    ("Judges 6:12", "The Lord is with thee, thou mighty man of valour."),

    # Day 221
    ("Ruth 2:12", "The Lord recompense thy work, and a full reward be given thee of the Lord."),

    # Day 222
    ("1 Samuel 2:2", "There is none holy as the Lord: for there is none beside Thee."),

    # Day 223
    ("1 Samuel 12:24", "Only fear the Lord, and serve Him in truth with all your heart."),

    # Day 224
    ("2 Samuel 7:22", "Thou art great, O Lord God: for there is none like Thee."),

    # Day 225
    ("1 Kings 2:3", "Keep the charge of the Lord thy God, to walk in His ways."),

    # Day 226
    ("1 Chronicles 16:11", "Seek the Lord and His strength, seek His face continually."),

    # Day 227
    ("1 Chronicles 16:34", "O give thanks unto the Lord; for He is good; for His mercy endureth for ever."),

    # Day 228
    ("2 Chronicles 15:7", "Be ye strong therefore, and let not your hands be weak."),

    # Day 229
    ("Ezra 8:23", "We fasted and besought our God for this: and He was intreated of us."),

    # Day 230
    ("Nehemiah 9:5", "Blessed be Thy glorious name, which is exalted above all blessing and praise."),

    # Day 231
    ("Esther 4:14", "Who knoweth whether thou art come to the kingdom for such a time as this?"),

    # Day 232
    ("Job 1:21", "The Lord gave, and the Lord hath taken away; blessed be the name of the Lord."),

    # Day 233
    ("Psalm 16:8", "I have set the Lord always before me: because He is at my right hand, I shall not be moved."),

    # Day 234
    ("Psalm 18:2", "The Lord is my rock, and my fortress, and my deliverer."),

    # Day 235
    ("Psalm 19:14", "Let the words of my mouth, and the meditation of my heart, be acceptable in Thy sight."),

    # Day 236
    ("Psalm 30:5", "Weeping may endure for a night, but joy cometh in the morning."),

    # Day 237
    ("Psalm 56:3", "What time I am afraid, I will trust in Thee."),

    # Day 238
    ("Psalm 63:1", "O God, Thou art my God; early will I seek Thee."),

    # Day 239
    ("Psalm 84:11", "The Lord God is a sun and shield: no good thing will He withhold from them that walk uprightly."),

    # Day 240
    ("Psalm 86:11", "Teach me Thy way, O Lord; I will walk in Thy truth."),    # Day 241
    ("Psalm 91:1", "He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty."),

    # Day 242
    ("Psalm 91:4", "He shall cover thee with His feathers, and under His wings shalt thou trust."),

    # Day 243
    ("Psalm 103:2", "Bless the Lord, O my soul, and forget not all His benefits."),

    # Day 244
    ("Psalm 105:4", "Seek the Lord, and His strength: seek His face evermore."),

    # Day 245
    ("Psalm 112:7", "He shall not be afraid of evil tidings: his heart is fixed, trusting in the Lord."),

    # Day 246
    ("Psalm 115:15", "Ye are blessed of the Lord which made heaven and earth."),

    # Day 247
    ("Psalm 119:105", "Thy word is a lamp unto my feet, and a light unto my path."),

    # Day 248
    ("Psalm 127:3", "Children are an heritage of the Lord: and the fruit of the womb is His reward."),

    # Day 249
    ("Psalm 128:1", "Blessed is every one that feareth the Lord; that walketh in His ways."),

    # Day 250
    ("Psalm 133:1", "Behold, how good and how pleasant it is for brethren to dwell together in unity."),

    # Day 251
    ("Proverbs 3:5", "Trust in the Lord with all thine heart; and lean not unto thine own understanding."),

    # Day 252
    ("Proverbs 3:6", "In all thy ways acknowledge Him, and He shall direct thy paths."),

    # Day 253
    ("Proverbs 8:17", "I love them that love Me; and those that seek Me early shall find Me."),

    # Day 254
    ("Proverbs 9:10", "The fear of the Lord is the beginning of wisdom."),

    # Day 255
    ("Proverbs 14:23", "In all labour there is profit: but the talk of the lips tendeth only to poverty."),

    # Day 256
    ("Proverbs 18:10", "The name of the Lord is a strong tower: the righteous runneth into it, and is safe."),

    # Day 257
    ("Proverbs 21:21", "He that followeth after righteousness and mercy findeth life, righteousness, and honour."),

    # Day 258
    ("Proverbs 31:25", "Strength and honour are her clothing; and she shall rejoice in time to come."),

    # Day 259
    ("Ecclesiastes 3:1", "To every thing there is a season, and a time to every purpose under the heaven."),

    # Day 260
    ("Ecclesiastes 4:9", "Two are better than one; because they have a good reward for their labour."),

    # Day 261
    ("Song of Solomon 2:4", "He brought me to the banqueting house, and His banner over me was love."),

    # Day 262
    ("Isaiah 9:6", "Unto us a child is born, unto us a Son is given: and His name shall be called Wonderful."),

    # Day 263
    ("Isaiah 12:2", "Behold, God is my salvation; I will trust, and not be afraid."),

    # Day 264
    ("Isaiah 40:8", "The grass withereth, the flower fadeth: but the word of our God shall stand for ever."),

    # Day 265
    ("Isaiah 40:31", "They that wait upon the Lord shall renew their strength; they shall mount up with wings as eagles."),

    # Day 266
    ("Isaiah 42:9", "Behold, the former things are come to pass, and new things do I declare."),

    # Day 267
    ("Isaiah 43:19", "Behold, I will do a new thing; now it shall spring forth."),

    # Day 268
    ("Isaiah 55:8", "My thoughts are not your thoughts, neither are your ways My ways, saith the Lord."),

    # Day 269
    ("Isaiah 58:11", "The Lord shall guide thee continually, and satisfy thy soul in drought."),

    # Day 270
    ("Isaiah 60:1", "Arise, shine; for thy light is come, and the glory of the Lord is risen upon thee."),    # Day 271
    ("Jeremiah 10:6", "There is none like unto Thee, O Lord; Thou art great, and Thy name is great in might."),

    # Day 272
    ("Jeremiah 31:3", "Yea, I have loved thee with an everlasting love: therefore with lovingkindness have I drawn thee."),

    # Day 273
    ("Jeremiah 32:27", "Behold, I am the Lord, the God of all flesh: is there any thing too hard for Me?"),

    # Day 274
    ("Jeremiah 33:6", "Behold, I will bring it health and cure, and I will cure them, and will reveal unto them abundance of peace and truth."),

    # Day 275
    ("Lamentations 3:25", "The Lord is good unto them that wait for Him, to the soul that seeketh Him."),

    # Day 276
    ("Ezekiel 34:26", "I will make them and the places round about My hill a blessing."),

    # Day 277
    ("Daniel 2:20", "Blessed be the name of God for ever and ever: for wisdom and might are His."),

    # Day 278
    ("Daniel 6:27", "He delivereth and rescueth, and He worketh signs and wonders in heaven and in earth."),

    # Day 279
    ("Hosea 14:4", "I will heal their backsliding, I will love them freely."),

    # Day 280
    ("Joel 2:13", "Return unto the Lord your God: for He is gracious and merciful, slow to anger, and of great kindness."),

    # Day 281
    ("Amos 9:14", "I will bring again the captivity of My people, and they shall build the waste cities, and inhabit them."),

    # Day 282
    ("Micah 7:7", "Therefore I will look unto the Lord; I will wait for the God of my salvation."),

    # Day 283
    ("Habakkuk 3:19", "The Lord God is my strength, and He will make my feet like hinds' feet."),

    # Day 284
    ("Zephaniah 2:3", "Seek ye the Lord, all ye meek of the earth; seek righteousness, seek meekness."),

    # Day 285
    ("Zechariah 9:9", "Rejoice greatly, O daughter of Zion; behold, thy King cometh unto thee."),

    # Day 286
    ("Malachi 4:2", "Unto you that fear My name shall the Sun of righteousness arise with healing in His wings."),

    # Day 287
    ("Matthew 5:8", "Blessed are the pure in heart: for they shall see God."),

    # Day 288
    ("Matthew 9:29", "According to your faith be it unto you."),

    # Day 289
    ("Matthew 10:39", "He that findeth his life shall lose it: and he that loseth his life for My sake shall find it."),

    # Day 290
    ("Matthew 16:26", "For what is a man profited, if he shall gain the whole world, and lose his own soul?"),

    # Day 291
    ("Matthew 19:14", "Suffer little children, and forbid them not, to come unto Me: for of such is the kingdom of heaven."),

    # Day 292
    ("Matthew 24:35", "Heaven and earth shall pass away, but My words shall not pass away."),

    # Day 293
    ("Mark 5:36", "Be not afraid, only believe."),

    # Day 294
    ("Mark 12:30", "Thou shalt love the Lord thy God with all thy heart, and with all thy soul."),

    # Day 295
    ("Luke 5:32", "I came not to call the righteous, but sinners to repentance."),

    # Day 296
    ("Luke 10:27", "Thou shalt love the Lord thy God with all thy heart, and thy neighbour as thyself."),

    # Day 297
    ("Luke 19:10", "The Son of man is come to seek and to save that which was lost."),

    # Day 298
    ("John 3:16", "For God so loved the world, that He gave His only begotten Son."),

    # Day 299
    ("John 8:12", "I am the light of the world: he that followeth Me shall not walk in darkness."),

    # Day 300
    ("John 10:10", "I am come that they might have life, and that they might have it more abundantly."),    # Day 301
    ("John 14:1", "Let not your heart be troubled: ye believe in God, believe also in Me."),

    # Day 302
    ("John 14:6", "I am the way, the truth, and the life: no man cometh unto the Father, but by Me."),

    # Day 303
    ("John 14:27", "Peace I leave with you, My peace I give unto you: let not your heart be troubled."),

    # Day 304
    ("John 15:12", "This is My commandment, That ye love one another, as I have loved you."),

    # Day 305
    ("John 16:24", "Ask, and ye shall receive, that your joy may be full."),

    # Day 306
    ("Acts 1:8", "Ye shall receive power, after that the Holy Ghost is come upon you."),

    # Day 307
    ("Acts 4:12", "Neither is there salvation in any other: for there is none other name under heaven given among men."),

    # Day 308
    ("Acts 16:31", "Believe on the Lord Jesus Christ, and thou shalt be saved."),

    # Day 309
    ("Romans 5:8", "God commendeth His love toward us, in that, while we were yet sinners, Christ died for us."),

    # Day 310
    ("Romans 8:1", "There is therefore now no condemnation to them which are in Christ Jesus."),

    # Day 311
    ("Romans 8:28", "All things work together for good to them that love God."),

    # Day 312
    ("Romans 8:31", "If God be for us, who can be against us?"),

    # Day 313
    ("Romans 12:12", "Rejoicing in hope; patient in tribulation; continuing instant in prayer."),

    # Day 314
    ("Romans 12:21", "Be not overcome of evil, but overcome evil with good."),

    # Day 315
    ("1 Corinthians 10:13", "God is faithful, who will not suffer you to be tempted above that ye are able."),

    # Day 316
    ("1 Corinthians 13:4", "Charity suffereth long, and is kind; charity envieth not."),

    # Day 317
    ("1 Corinthians 13:13", "Now abideth faith, hope, charity, these three; but the greatest of these is charity."),

    # Day 318
    ("1 Corinthians 15:58", "Be ye stedfast, unmoveable, always abounding in the work of the Lord."),

    # Day 319
    ("2 Corinthians 1:3", "The Father of mercies, and the God of all comfort."),

    # Day 320
    ("2 Corinthians 5:17", "If any man be in Christ, he is a new creature: old things are passed away."),

    # Day 321
    ("2 Corinthians 9:8", "God is able to make all grace abound toward you."),

    # Day 322
    ("Galatians 2:20", "I am crucified with Christ: nevertheless I live; yet not I, but Christ liveth in me."),

    # Day 323
    ("Galatians 6:9", "Let us not be weary in well doing: for in due season we shall reap."),

    # Day 324
    ("Ephesians 3:20", "Unto Him that is able to do exceeding abundantly above all that we ask or think."),

    # Day 325
    ("Ephesians 4:32", "Be ye kind one to another, tenderhearted, forgiving one another."),

    # Day 326
    ("Philippians 1:6", "He which hath begun a good work in you will perform it until the day of Jesus Christ."),

    # Day 327
    ("Philippians 4:6", "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving."),

    # Day 328
    ("Philippians 4:7", "The peace of God, which passeth all understanding, shall keep your hearts and minds."),

    # Day 329
    ("Philippians 4:13", "I can do all things through Christ which strengtheneth me."),

    # Day 330
    ("Colossians 3:23", "Whatsoever ye do, do it heartily, as to the Lord, and not unto men."),    # Day 331
    ("Colossians 3:17", "Whatsoever ye do in word or deed, do all in the name of the Lord Jesus."),

    # Day 332
    ("1 Thessalonians 5:16", "Rejoice evermore."),

    # Day 333
    ("1 Thessalonians 5:17", "Pray without ceasing."),

    # Day 334
    ("1 Thessalonians 5:18", "In every thing give thanks: for this is the will of God in Christ Jesus concerning you."),

    # Day 335
    ("2 Thessalonians 3:3", "The Lord is faithful, who shall stablish you, and keep you from evil."),

    # Day 336
    ("1 Timothy 4:12", "Let no man despise thy youth; but be thou an example of the believers."),

    # Day 337
    ("2 Timothy 1:7", "God hath not given us the spirit of fear; but of power, and of love, and of a sound mind."),

    # Day 338
    ("Hebrews 4:12", "The word of God is quick, and powerful, and sharper than any twoedged sword."),

    # Day 339
    ("Hebrews 11:1", "Faith is the substance of things hoped for, the evidence of things not seen."),

    # Day 340
    ("Hebrews 11:6", "Without faith it is impossible to please Him: for he that cometh to God must believe that He is."),

    # Day 341
    ("Hebrews 12:1", "Let us run with patience the race that is set before us."),

    # Day 342
    ("Hebrews 12:2", "Looking unto Jesus the author and finisher of our faith."),

    # Day 343
    ("James 1:5", "If any of you lack wisdom, let him ask of God, that giveth to all men liberally."),

    # Day 344
    ("James 1:17", "Every good gift and every perfect gift is from above."),

    # Day 345
    ("James 1:22", "Be ye doers of the word, and not hearers only."),

    # Day 346
    ("James 2:17", "Faith, if it hath not works, is dead, being alone."),

    # Day 347
    ("1 Peter 2:24", "Who His own self bare our sins in His own body on the tree."),

    # Day 348
    ("1 Peter 3:15", "Sanctify the Lord God in your hearts: and be ready always to give an answer."),

    # Day 349
    ("1 Peter 5:8", "Be sober, be vigilant; because your adversary the devil walketh about."),

    # Day 350
    ("2 Peter 3:18", "Grow in grace, and in the knowledge of our Lord and Saviour Jesus Christ."),

    # Day 351
    ("1 John 2:5", "Whoso keepeth His word, in him verily is the love of God perfected."),

    # Day 352
    ("1 John 3:18", "Let us not love in word, neither in tongue; but in deed and in truth."),

    # Day 353
    ("1 John 4:16", "God is love; and he that dwelleth in love dwelleth in God."),

    # Day 354
    ("1 John 5:4", "This is the victory that overcometh the world, even our faith."),

    # Day 355
    ("Jude 1:2", "Mercy unto you, and peace, and love, be multiplied."),

    # Day 356
    ("Revelation 1:3", "Blessed is he that readeth, and they that hear the words of this prophecy."),

    # Day 357
    ("Revelation 4:11", "Thou art worthy, O Lord, to receive glory and honour and power."),

    # Day 358
    ("Revelation 7:17", "God shall wipe away all tears from their eyes."),

    # Day 359
    ("Revelation 19:6", "The Lord God omnipotent reigneth."),

    # Day 360
    ("Revelation 21:5", "Behold, I make all things new."),

    # Day 361
    ("Psalm 23:1", "The Lord is my shepherd; I shall not want."),

    # Day 362
    ("Psalm 27:1", "The Lord is my light and my salvation; whom shall I fear?"),

    # Day 363
    ("Psalm 34:8", "O taste and see that the Lord is good: blessed is the man that trusteth in Him."),

    # Day 364
    ("Psalm 37:5", "Commit thy way unto the Lord; trust also in Him; and He shall bring it to pass."),

    # Day 365
    ("Psalm 150:6", "Let every thing that hath breath praise the Lord. Praise ye the Lord."),
]
