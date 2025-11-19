import random
import datetime

# list of verses to be randomized daily
verses = {
    "John 3:16": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
    "Psalm 23:1": "The Lord is my shepherd; I shall not want.",
    "Proverbs 3:5": "Trust in the Lord with all thine heart; and lean not unto thine own understanding.",
    "Romans 8:28": "And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
    "Philippians 4:13": "I can do all things through Christ which strengtheneth me.",
    "Romans 5:8": "But God commendeth his love toward us, in that, while we were yet sinners, Christ died for us.",
    "Jeremiah 31:3": "The Lord hath appeared of old unto me, saying, Yea, I have loved thee with an everlasting love: therefore with lovingkindness have I drawn thee.",
    "Joshua 1:9": "Have not I commanded thee? Be strong and of a good courage; be not afraid, neither be thou dismayed: for the Lord thy God is with thee whithersoever thou goest.",
    "Isaiah 41:10": "Fear thou not; for I am with thee: be not dismayed; for I am thy God: I will strengthen thee; yea, I will help thee; yea, I will uphold thee with the right hand of my righteousness.",
    "Psalm 27:1": "The Lord is my light and my salvation; whom shall I fear? the Lord is the strength of my life; of whom shall I be afraid?",
    "Deuteronomy 31:6": "Be strong and of a good courage, fear not, nor be afraid of them: for the Lord thy God, he it is that doth go with thee; he will not fail thee, nor forsake thee.",
    "John 14:27": "Peace I leave with you, my peace I give unto you: let not your heart be troubled, neither let it be afraid.",
    "Philippians 4:7": "And the peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus.",
    "Isaiah 26:3": "Thou wilt keep him in perfect peace, whose mind is stayed on thee: because he trusteth in thee.",
    "Colossians 3:15": "And let the peace of God rule in your hearts, to the which also ye are called in one body; and be ye thankful.",
    "Psalm 4:8": "I will both lay me down in peace, and sleep: for thou, Lord, only makest me dwell in safety.",
    "Psalm 56:3": "What time I am afraid, I will trust in thee.",
    "Psalm 37:5": "Commit thy way unto the Lord; trust also in him; and he shall bring it to pass.",
    "Nahum 1:7": "The Lord is good, a strong hold in the day of trouble; and he knoweth them that trust in him.",
    "Romans 15:13": "Now the God of hope fill you with all joy and peace in believing, that ye may abound in hope, through the power of the Holy Ghost.",
    "Jeremiah 29:11": "For I know the thoughts that I think toward you, saith the Lord, thoughts of peace, and not of evil, to give you an expected end.",
    "Psalm 42:11": "Why art thou cast down, O my soul? and why art thou disquieted within me? hope thou in God: for I shall yet praise him, who is the health of my countenance, and my God.",
    "1 Peter 1:3": "Blessed be the God and Father of our Lord Jesus Christ, which according to his abundant mercy hath begotten us again unto a lively hope by the resurrection of Jesus Christ from the dead.",
    "Hebrews 11:1": "Now faith is the substance of things hoped for, the evidence of things not seen.",
    "2 Corinthians 5:7": "For we walk by faith, not by sight.",
    "Galatians 2:20": "I am crucified with Christ: nevertheless I live; yet not I, but Christ liveth in me: and the life which I now live in the flesh I live by the faith of the Son of God, who loved me, and gave himself for me.",
    "Mark 11:24": "Therefore I say unto you, What things soever ye desire, when ye pray, believe that ye receive them, and ye shall have them.",
    "Romans 1:17": "For therein is the righteousness of God revealed from faith to faith: as it is written, The just shall live by faith.",
    "Isaiah 40:31": "But they that wait upon the Lord shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint.",
    "John 16:33": "These things I have spoken unto you, that in me ye might have peace. In the world ye shall have tribulation: but be of good cheer; I have overcome the world.",
    "Psalm 46:1": "God is our refuge and strength, a very present help in trouble.",
    "2 Corinthians 12:9": "And he said unto me, My grace is sufficient for thee: for my strength is made perfect in weakness.",
    "Psalm 32:8": "I will instruct thee and teach thee in the way which thou shalt go: I will guide thee with mine eye.",
    "Isaiah 58:11": "And the Lord shall guide thee continually, and satisfy thy soul in drought, and make fat thy bones...",
    "Psalm 119:105": "Thy word is a lamp unto my feet, and a light unto my path.",
    "Proverbs 16:9": "A man's heart deviseth his way: but the Lord directeth his steps.",
    "James 1:5": "If any of you lack wisdom, let him ask of God, that giveth to all men liberally...",
    "1 Thessalonians 5:18": "In every thing give thanks: for this is the will of God in Christ Jesus concerning you.",
    "Psalm 107:1": "O give thanks unto the Lord, for he is good: for his mercy endureth for ever.",
    "Colossians 3:17": "And whatsoever ye do in word or deed, do all in the name of the Lord Jesus, giving thanks to God and the Father by him.",
    "Psalm 118:24": "This is the day which the Lord hath made; we will rejoice and be glad in it.",
    "Ephesians 5:20": "Giving thanks always for all things unto God and the Father in the name of our Lord Jesus Christ."
}

def get_verse_of_the_day():
    # seed the randomness using today's date (changes daily)
    random.seed(datetime.date.today().toordinal())

    randomized = random.choice(list(verses.keys()))
    return [randomized, verses[randomized]]

votd = get_verse_of_the_day()

